# Central-server usage

Use `skig-server` when a team needs a shared graph with centrally managed access.
The server stores the authoritative graph in PostgreSQL. CLI commands and MCP
tools use the same selected graph and access grants.

The v0.0.303 public release is an alpha and is not production ready. Its server binary passes a version
contract smoke check; this release does not claim new server deployment
qualification, full remote CLI parity or broader migration capability.

## Deployment requirements

See [server setup and configuration](https://github.com/avastmick/skig/wiki/Server-setup)
for the administrator sequence, runtime settings and current bootstrap gaps.
The public release does not automatically initialise PostgreSQL or Keycloak.

An administrator provides:

- A compatible `skig-server` release and PostgreSQL database.
- An OAuth 2.0 / OpenID Connect identity provider.
- HTTPS for remote access; explicit local deployments can use loopback HTTP.
- A provisioned graph, its registration and access grants.
- Client configuration and the matching SKIG toolchain version.

Use `skig-server --help` and the selected release's deployment instructions for
configuration options. Installing the server binary or registering an account
does not provision a graph or grant access to it.

## Connect a project

Obtain `.skig/authority-config.json` from your administrator. It selects
`local_server` or `remote_server` and identifies the endpoint and registered
graph. Use the supplied identities; do not invent them or put credentials in
this file.

Inside the configured project, run:

```bash
skig auth login
skig auth status
skig task available
skig req query
```

Open the displayed URL and enter the device code to sign in. SKIG stores the
renewable credential privately under `$XDG_CONFIG_HOME/skig/auth`, normally
`~/.config/skig/auth`, and refreshes it automatically. SKIG does not ask for or
store your account password.

Signing in establishes your identity. Your administrator grants access to the
graph separately. Use `skig auth status` to check that access, and
`skig auth logout` to revoke and remove the saved renewable credential.

## How this differs from Git mode

Supported commands read and update the server's graph directly. The client does
not keep a local authoritative graph or persistent graph cache. Unsupported
operations and connection failures return errors rather than switching to Git
storage. Your application code can still live in Git.

Moving an existing Git graph to a server requires a governed migration; changing
the configuration file alone is not a migration. Coordinate the move with your
administrator and follow the release's migration instructions.

## Applications and automation

Applications can use an administrator-supplied configuration independently of
the current directory:

```bash
skig --config /absolute/path/application.json task available
```

Unattended applications use a separate confidential OAuth client and narrowly
granted graph access. Keep client secrets in private files outside the
repository. Have the administrator supply the appropriate credential reference
rather than reusing a person's login.
