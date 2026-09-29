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

- **Linux:** x86_64 with glibc 2.39 or newer and `libgcc_s.so.1`.
- **macOS:** support will follow.
- **Windows:** no native support is planned. Run the Linux version inside Windows
  Subsystem for Linux (WSL), using a compatible x86_64 Linux environment.

## Install

**SKIG v3.0.2 is an alpha release and is not production ready.**
See [release notes](https://github.com/avastmick/skig/releases/tag/v3.0.2)
for requirements and limitations. Alpine/musl and ARM are not supported.

Install with Bash and curl:

```bash
curl --proto '=https' --tlsv1.2 -fsSL \
  https://raw.githubusercontent.com/avastmick/skig/main/scripts/install.sh \
  | SKIG_VERSION=3.0.2 bash
export PATH="$HOME/.local/bin:$PATH"
skig --version
```

The installer checks SHA-256 checksums and binary versions, then installs to
`~/.local/bin` without sudo. Set `SKIG_INSTALL_DIR` to choose another directory.
Add the `export PATH` line to your shell startup file if needed.

The dispatcher selects the version pinned by each project; older installed
versions are retained. No Rust toolchain or private source access is required.
See the [installation guide](https://github.com/avastmick/skig/wiki/Installation)
for manual installation and upgrades.

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
