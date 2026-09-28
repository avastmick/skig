# Installation

SKIG initially supports Linux x86_64. On Windows, run these steps inside a
compatible WSL Linux environment. macOS support will follow.

## Download and verify

Open [Releases](https://github.com/avastmick/skig/releases) and choose a version.
If no release is listed, public binaries are not yet available.

Download these assets from the same release into an empty directory:

- `skig-linux-x86_64`
- `skig-dispatcher-linux-x86_64`
- `SHA256SUMS`

In that directory, run:

```bash
sha256sum --ignore-missing --check SHA256SUMS
```

Continue only when both downloaded binaries report `OK`.

## Install the CLI

Replace `X.Y.Z` with the release version without its `v` prefix:

```bash
VERSION=X.Y.Z
mkdir -p "$HOME/.local/bin"
install -m 0755 skig-linux-x86_64 "$HOME/.local/bin/skig-v$VERSION"
install -m 0755 skig-dispatcher-linux-x86_64 "$HOME/.local/bin/skig"
export PATH="$HOME/.local/bin:$PATH"
skig --version
```

Add the `export PATH` line to your shell startup file if needed. No Rust
toolchain or access to SKIG's source code is required.

The `skig` dispatcher selects the version pinned by a project. Repeat these
steps to install another release, keeping older `skig-vX.Y.Z` binaries for
projects that still use them. Installing a binary does not migrate a project's
data or change its version pin; follow the selected release's migration notes.

## Optional server binary

Administrators also need `skig-server-linux-x86_64`. Download it and `SHA256SUMS`
from the same release, verify that the server asset reports `OK` using the
checksum command above, then run:

```bash
install -m 0755 skig-server-linux-x86_64 "$HOME/.local/bin/skig-server"
skig-server --help
```

The binary alone does not create a working deployment. See
[central-server usage](https://github.com/avastmick/skig/wiki/Central-server)
for the required services and client setup.
