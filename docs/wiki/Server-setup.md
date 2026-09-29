# Server setup and configuration

**SKIG v3.0.2 is an alpha release and is not production ready.** Server setup
currently requires an administrator-managed deployment. The public release does
not include a complete PostgreSQL/Keycloak bootstrap package.

The CLI installer installs the CLI and dispatcher. Installing the optional
`skig-server` binary does **not** start PostgreSQL, configure an identity provider,
create a usable graph or grant anyone access.

## Services to prepare

An administrator must supply and operate:

- **PostgreSQL:** a dedicated database, a schema-owner credential for initial
  setup, and a separate runtime role without superuser, row-security bypass,
  database creation or role creation privileges.
- **An OIDC identity provider, such as Keycloak:** a realm/issuer, signing keys,
  clients, token audience and scopes. SKIG does not install or start Keycloak.
- **An OpenTelemetry collector:** the server requires an OTLP endpoint.
- **Network access and persistent storage:** HTTPS for remote clients, database
  storage, private credentials and a tested backup/restore process.

The alpha does not publish a qualified standalone combination of PostgreSQL and
Keycloak versions, container manifests or a ready-to-import realm. Internal
development deployment recipes are not part of the public downloads.

## Administrator setup sequence

This is the sequence of available server operations, not a complete copy-and-paste
bootstrap. Provisioning documents, identities and credentials must come from
your deployment.

1. [Install the server binary](https://github.com/avastmick/skig/wiki/Installation#optional-server-binary)
   and inspect `skig-server --help`.
2. Create the PostgreSQL database and roles. Supply database credentials privately
   through `SKIG_SERVER_DATABASE_URL`.
3. Choose the database mode **before initialisation**. For a new, empty alpha
   database using scheduled database backups, run
   `skig-server initialise-database-backup` with the owner credential. It creates
   the schema and records the mode; the current schema must be `public`.
   Do not run `migrate` first: ordinary migration
   selects the separate protected mode. These modes are not interchangeable.
4. Configure the identity provider and obtain the authorised provisioning actor's
   token. `skig-server grant` permits an exact principal to provision an absent
   graph; it does not create that graph.
5. Use `skig-server genesis` to emit a new empty graph's revision-zero backup.
   This does not include a preconfigured SKIG core ontology. Review the backup
   and a `crepuscular.skig.provisioning/v2` request, including
   registration and initial grants, then apply them with `skig-server provision`.
   Provisioning requires both the authenticated Restore scope and the exact grant.
6. Create the runtime selection from the actual registration. Database-backup
   mode uses contract `skig.hosted-database-backup.v1`, with a non-empty `modules`
   array whose entries contain a `source` authority reference.
7. Switch to the runtime database credential, supply the configuration below,
   and start `skig-server serve-registered --database-backup --selection-file selection.json`.
8. Check `/livez` and `/readyz`. Grant each user the required operations with
   `skig-server grant-existing`, then supply the matching client configuration.

Use `skig-server <command> --help` for each command's required inputs. A successful
`version` command verifies the binary, not database or deployment readiness.
Public seed/request generation and a complete first-graph demonstration remain
deployment gaps. The empty-database initialiser refuses repeat use; do not run it
as a normal startup command.

Protected mode additionally requires a `skig.hosted-runtime.v1` selection with
trusted checkpoints and private recovery directories. Running `migrate` alone
does not prepare a registered service for startup.

In database-backup mode, the runtime role needs database `CONNECT`, schema
`USAGE`, `SELECT`/`INSERT`/`UPDATE` on the fifteen namespace tables, read access
to mode/migration metadata, and execution of product functions. It must not have
`DELETE`, `TRUNCATE`, DDL privileges or owner/backup role membership. The release
does not include a role-bootstrap SQL manifest. Namespace tables retain forced
row-level security.

## Runtime configuration

| Environment variable | Value supplied by the administrator |
| --- | --- |
| `SKIG_SERVER_DATABASE_URL` | Private runtime PostgreSQL connection string |
| `SKIG_SERVER_HOSTED_SELECTION_FILE` | Path to the registered-module selection JSON |
| `SKIG_SERVER_OIDC_ISSUER` | Exact issuer in signed tokens |
| `SKIG_SERVER_OIDC_AUDIENCE` | Expected access-token audience |
| `SKIG_SERVER_OIDC_JWKS_URI` | Signing-key endpoint |
| `SKIG_SERVER_PROTECTED_RESOURCE` | Public protected-resource identifier |
| `SKIG_SERVER_LISTEN_ADDRESS` | Bind address; default `127.0.0.1:8080` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Reachable telemetry endpoint |
| `SKIG_SERVER_DEPLOYMENT_ENVIRONMENT` | Deployment environment identifier |

For human CLI login, the default public OAuth client is `skig-cli`. It needs
device authorisation and renewable credentials, with the requested scopes
`openid`, `offline_access`, `skig:query`, `skig:mutate` and
`skig:consequence:repository-change`. The server verifies RS256-signed tokens
against its configured issuer, audience and keys. OAuth scopes do not replace
per-graph grants.

The identity provider must expose discovery, device authorisation, token,
revocation and JWKS endpoints. Configure token audience and scope mappings, with
client identity in `azp` or `client_id`. Use a separate administrative identity
with `skig:restore` for provisioning.

The server listens over HTTP; remote HTTPS requires an administrator-managed
reverse proxy or equivalent TLS termination. The registered selection's `source`
contains `organisation_id`, `module_id`, `graph_id`, `graph_iri`, `authority` and
`profile`, copied from the actual registration.

Database-backup runtime mode optionally accepts `SKIG_SERVER_POC_HTTP_JWKS_URI`
for one explicitly trusted HTTP key endpoint, exactly matching the configured
JWKS URI. This runtime-only exception does not apply to `provision`, which uses
the normal verifier requiring HTTPS or loopback HTTP for key retrieval.

## Client configuration template

The administrator supplies `.skig/authority-config.json`. Replace every angle-bracket
placeholder below with its actual registered value; this template is not usable
unchanged:

```json
{
  "contract": "skig.authority-configuration.v1",
  "organisation_id": "<registered UUIDv7>",
  "module_id": "<registered UUIDv7>",
  "graph_id": "<registered UUIDv7>",
  "graph_iri": "<registered absolute graph IRI>",
  "generation": "<registered authority-generation UUIDv7>",
  "local_runtime": {"root": ".skig/runtime"},
  "mode": {
    "kind": "local_server",
    "endpoint": "http://127.0.0.1:8080",
    "credential_ref": "env:SKIG_ACCESS_TOKEN"
  }
}
```

For remote access, use `remote_server` and the server's HTTPS origin. The credential
reference permits saved-session login; do not replace it with a token or commit
credentials. The client also needs the matching toolchain pin.

## Storage, restart and client connection

Retain PostgreSQL data, Keycloak's database/configuration, registration identities,
selection files and private credentials across restarts. Protected mode also
requires its recovery files. Restart under a service supervisor with the same
runtime identity and selection, without rerunning initialisation or provisioning.
Database-backup mode relies on an externally scheduled full
database backup every 15 minutes and a demonstrated restore to a separate
database. The server does not create that schedule; data loss between backups
is possible, and the schedule does not guarantee a 15-minute loss bound.

Client projects need an administrator-supplied `.skig/authority-config.json`
matching the registered graph and a compatible toolchain pin. Follow
[central-server usage](https://github.com/avastmick/skig/wiki/Central-server)
for login and access checks.

The alpha does not claim full remote CLI parity or a generally available
Git-to-server migration. Creating or seeding a graph is not proof of a
history-preserving migration.

This reference was checked against the released v3.0.2 command help and tagged
source contracts. A fresh-machine PostgreSQL/Keycloak deployment was not
performed or qualified for this guide.
