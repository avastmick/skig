#!/usr/bin/env bash
# Install public SKIG binaries. Run with Bash; no elevated privileges are needed.
set -euo pipefail

fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }

download() {
    curl --fail --silent --show-error --location --retry 2 \
        --proto '=https' --proto-redir '=https' --tlsv1.2 "$@"
}

cleanup() {
    if [[ -n ${staging:-} ]]; then rm -rf -- "$staging"; fi
    if [[ -n ${lock_dir:-} ]]; then rmdir -- "$lock_dir"; fi
}

main() {
    [[ $(uname -s) == Linux && $(uname -m) == x86_64 ]] ||
        fail 'Only Linux x86_64 is supported. On Windows, run inside x86_64 WSL.'
    for dependency in curl sha256sum awk mktemp install chmod mv ln mkdir rmdir rm; do
        command -v "$dependency" >/dev/null || fail "Missing required command: $dependency"
    done

    requested=${SKIG_VERSION:-latest}
    release_root=https://github.com/avastmick/skig/releases
    if [[ $requested == latest ]]; then
        # Resolve once so all assets come from the same release, even during updates.
        resolved=$(download --output /dev/null --write-out '%{url_effective}' \
            "$release_root/latest") ||
            fail 'No latest release is available. Check Releases or set SKIG_VERSION explicitly.'
        [[ $resolved == "$release_root/tag/"* ]] || fail 'Unexpected latest-release URL.'
        requested=${resolved##*/}
    fi
    version=${requested#v}
    [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] ||
        fail 'SKIG_VERSION must be latest or a release version such as 3.0.2.'

    destination=${SKIG_INSTALL_DIR:-${HOME:?HOME is required}/.local/bin}
    mkdir -p -- "$destination"
    destination=$(cd -- "$destination" && pwd -P)
    # Serialise installers and stage on the destination filesystem for atomic moves.
    mkdir -- "$destination/.skig-install.lock" 2>/dev/null ||
        fail "Install lock exists: $destination/.skig-install.lock. Check for another installer."
    lock_dir=$destination/.skig-install.lock
    trap cleanup EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    staging=$(mktemp -d "$destination/.skig-download.XXXXXXXX")
    cd -- "$staging"

    for asset in skig-linux-x86_64 skig-dispatcher-linux-x86_64 SHA256SUMS; do
        download "$release_root/download/v$version/$asset" --output "$asset" ||
            fail "Could not download $asset for v$version. Check the Releases page."
    done
    # Select exactly the two required entries; never trust paths in a remote manifest.
    for asset in skig-linux-x86_64 skig-dispatcher-linux-x86_64; do
        checksum=$(awk -v name="$asset" '$2 == name {print $1}' SHA256SUMS)
        [[ $checksum =~ ^[[:xdigit:]]{64}$ ]] || fail "Missing or ambiguous checksum for $asset."
        printf '%s  %s\n' "$checksum" "$asset" | sha256sum --check --status ||
            fail "Checksum verification failed for $asset."
    done
    chmod 0755 skig-linux-x86_64 skig-dispatcher-linux-x86_64
    reported=$(./skig-linux-x86_64 --version) || fail 'The downloaded CLI cannot run on this system.'
    [[ $reported == "skig $version" ]] || fail "Unexpected CLI version: $reported"
    mv skig-linux-x86_64 "skig-v$version"
    mv skig-dispatcher-linux-x86_64 skig
    reported=$(./skig --version) || fail 'The downloaded dispatcher cannot run on this system.'
    [[ $reported == "skig $version" ]] || fail "Unexpected dispatcher version: $reported"

    target=$destination/skig-v$version
    if [[ -e $target || -L $target ]]; then
        [[ -f $target && ! -L $target && -x $target ]] || fail "Not an executable regular file: $target"
        existing=$(sha256sum "$target")
        incoming=$(sha256sum "skig-v$version")
        [[ ${existing%% *} == "${incoming%% *}" ]] || fail "Existing version differs: $target"
    else
        # A hard link publishes the complete file without overwriting a raced creation.
        ln -- "skig-v$version" "$target"
    fi
    [[ ! -d $destination/skig ]] || fail "Installation target is a directory: $destination/skig"
    mv -fT -- skig "$destination/skig"
    printf 'Installed SKIG %s in %s\n' "$version" "$destination"
    printf 'Ensure this directory is on PATH, then run: skig --version\n'
}

main "$@"
