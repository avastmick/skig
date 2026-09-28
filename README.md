# SKIG — System Knowledge and Intent Graph

SKIG connects a project's requirements, architecture decisions, constraints,
tasks, code, tests and evidence in a shared knowledge graph. It helps people and
AI agents understand what a system should do, why it exists and how its
implementation meets that intent.

Use the command-line interface for everyday work and automation, or the Model
Context Protocol (MCP) server for agent integration. Validation covers schema,
semantics, traceability and governance.

SKIG is **free of charge to download and use**. This repository hosts public
releases, documentation and issue reports. Development takes place in a private
repository; source code is not published and code contributions are not accepted.
Bug reports and suggestions are welcome.

## Platforms

- **Linux:** supported initially, with x86_64 binaries.
- **macOS:** support will follow.
- **Windows:** no native support is planned. Run the Linux version inside Windows
  Subsystem for Linux (WSL), using a compatible x86_64 Linux environment.

## Install

Public binaries will appear on the [Releases page](https://github.com/avastmick/skig/releases).
No public release has been published yet.

Once a release is available:

1. Download `skig-linux-x86_64`, `skig-dispatcher-linux-x86_64` and `SHA256SUMS`
   from the **same release** into an empty directory.
2. In that directory, verify the downloads:

   ```bash
   sha256sum --ignore-missing --check SHA256SUMS
   ```

   Continue only when both downloaded binaries report `OK`.
3. Install them, replacing `X.Y.Z` with the release version without its `v` prefix:

   ```bash
   VERSION=X.Y.Z
   mkdir -p "$HOME/.local/bin"
   install -m 0755 skig-linux-x86_64 "$HOME/.local/bin/skig-v$VERSION"
   install -m 0755 skig-dispatcher-linux-x86_64 "$HOME/.local/bin/skig"
   export PATH="$HOME/.local/bin:$PATH"
   skig --version
   ```

Add the `export PATH` line to your shell startup file if needed. The dispatcher
selects the version pinned by each project; keep older versioned binaries when
other projects still need them. Installation requires no Rust toolchain or
access to SKIG's source code.

## Use with Git

Run these commands inside your own Git repository:

```bash
skig init
skig install
skig req add --category CLI --title "Display command help" \
  --description "Show usage and available commands when invoked with --help."
skig req query
```

`skig install` adds Git hooks and agent skills. Commit the generated project
metadata and tracked `.skig/` records alongside your code, then share changes
through your normal Git workflow. JSON and NDJSON records preserve the graph;
SQLite is a disposable local query cache. This mode needs no central SKIG server.

## Use a central server

Teams can run **`skig-server`**, backed by PostgreSQL, to hold a shared graph and
manage access centrally. The CLI and MCP integration connect to that server.

Your administrator provisions the graph, grants access and supplies the project's
`.skig/authority-config.json`, selecting `local_server` or `remote_server`.
Remote connections use HTTPS. In the configured project, run:

```bash
skig auth login
skig auth status
skig task available
```

Follow the displayed URL and device code to sign in through the deployment's
identity provider. Signing in does not itself grant graph access. Credentials
are stored privately outside the repository and refreshed automatically.

In server mode, the server holds the authoritative graph. Supported commands
read and update it directly; a connection failure does not switch to local Git
storage. Administrators can download `skig-server-linux-x86_64` from the same
release and inspect deployment options with `skig-server --help` after installation.

## Supported standards

SKIG's ontology profile uses defined subsets of these standards:

| Standard | Use in SKIG |
| --- | --- |
| RDF 1.1 and N-Quads 1.1 | Graph model and RDF serialisation |
| OWL 2 RL | Bounded ontology reasoning |
| SHACL Core | Shape validation, alongside SKIG constraints |
| JSON-LD 1.1 | Graph exchange |
| PROV-O | Provenance alignment |
| RDFC-1.0 | Canonical RDF datasets |
| SPARQL 1.1 Query | Read-only server queries |

These are profile-scoped capabilities, not unrestricted implementations of every
standard. Graph changes go through SKIG commands; SPARQL Update is not supported.
Agent integration uses MCP, and server authentication uses OAuth 2.0 and OpenID
Connect (OIDC).

## Help and feedback

Use `skig --help` or `skig <command> --help` for command details. See the
[Wiki](https://github.com/avastmick/skig/wiki) for installation and usage guides.

Report problems or suggest improvements in
[Issues](https://github.com/avastmick/skig/issues). Include your SKIG version,
Linux distribution or WSL environment, steps to reproduce, and expected and
actual behaviour. Remove credentials and private project data from logs.
