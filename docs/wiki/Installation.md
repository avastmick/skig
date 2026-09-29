# Installation

SKIG v0.0.303 is an **alpha release and is not production ready**.
It requires Linux x86_64, glibc 2.39 or newer, `libgcc_s.so.1`, and the standard
Linux x86_64 dynamic loader. Alpine/musl and ARM are not supported. On Windows,
use a compatible WSL Linux environment. macOS support will follow.

## Quick install

With Bash, curl and standard GNU command-line utilities installed, run:

```bash
curl --proto '=https' --tlsv1.2 -fsSL \
  https://raw.githubusercontent.com/avastmick/skig/main/scripts/install.sh \
  | SKIG_VERSION=0.0.303 bash
export PATH="$HOME/.local/bin:$PATH"
skig --version
```

You can [inspect the installer](https://github.com/avastmick/skig/blob/main/scripts/install.sh)
or download it and run it with Bash. It verifies checksums and binary versions
before installing the CLI and dispatcher. Failed download or validation leaves
an existing installation unchanged.

Set `SKIG_VERSION` to a published version and `SKIG_INSTALL_DIR` to a writable
destination to customise installation:

```bash
SKIG_VERSION=0.0.303 SKIG_INSTALL_DIR="$HOME/bin" bash install.sh
```

Without `SKIG_VERSION`, the installer selects v0.0.303 Alpha explicitly.
`SKIG_VERSION=latest` asks GitHub for a non-prerelease and does not select Alpha.
Add your chosen installation directory to `PATH`; no sudo is needed.

## Manual download and verification

Open [Releases](https://github.com/avastmick/skig/releases) and choose a version.
Read its release notes before installing.

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

## Existing v3.0.2 projects: explicit Alpha reset

The only supported reset is **v3.0.2 → v0.0.303**. It changes product
selection from `skig-v3` to `skig-v0`, preserving schema 5, ontology profile 2.0,
graph identities, graph/history bytes, configuration and grants. Both native Git
graphs and server-client repository metadata use the same explicit command.
This is not an ontology downgrade or transfer between storage modes.

Commit existing metadata and native graph work first. Install the verified new
binaries alongside the retained v3.0.2 executable. From the project worktree,
invoke the target directly; the dispatcher still honours the old pin:

```bash
"$HOME/.local/bin/skig-v0.0.303" migrate authority upgrade-toolchain --format json
"$HOME/.local/bin/skig-v0.0.303" migrate authority upgrade-toolchain --format json \
  --base '<reviewed-preview-base>' --decider '<actual-reviewer>' \
  --reason '<review-rationale>'
"$HOME/.local/bin/skig-v0.0.303" install
skig --version
```

Review the exact source pin, immutable backup, preserved-file/configuration
hashes and candidate executable/embedded-skill hashes before apply. Confirm the
selected `.agents/skills/skig-v0/SKILL.md`, then commit the pin, receipt and
installation metadata through normal hooks. Never hand-edit pins or reinstall
to force a version change. Unsupported versions, stale inputs and mismatched
replays fail closed; an exact apply retry is non-mutating.

For server use, administrators qualify/select the matching server executable
separately using their deployment tools, retaining the previous executable/image.
The metadata transition does not contact or migrate the server. Verify access
and an authorised ordinary command against the selected live server afterwards.
Standalone application configuration is application-owned, not a repository
pin upgrade. Do not assume a version response proves deployment readiness.

Keep old binaries and skills while hooks, pins or rollback reference them.
Retain the source commit, preview and decision. For deliberate metadata rollback,
retain receipts and subsequent work and use a reviewed Git revert of the
transition/installation commit; never restore a whole graph over later work.
Server rollback independently selects its retained executable/image. The reset
requires no data conversion or database restore.
