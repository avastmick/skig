# Supported standards

SKIG's ontology profile uses defined subsets of the following standards.
Support is profile-scoped rather than an unrestricted implementation of every
feature in each specification.

| Standard | Use |
| --- | --- |
| RDF 1.1 | Abstract graph and dataset model |
| N-Quads 1.1 | RDF dataset serialisation |
| OWL 2 RL | Bounded ontology reasoning |
| SHACL Core | Shape validation, alongside SKIG-specific constraints |
| JSON-LD 1.1 | Graph exchange |
| PROV-O | Provenance alignment |
| RDFC-1.0 | Canonical RDF datasets |
| SPARQL 1.1 Query | Read-only server queries |

The server supports `SELECT`, `ASK`, `CONSTRUCT` and `DESCRIBE` within its access,
revision and resource limits. Graph mutations go through SKIG commands;
SPARQL Update and direct dataset uploads are not mutation interfaces.

The same semantic graph model underlies Git and PostgreSQL storage. Exported RDF
and JSON-LD describe that graph; exporting it does not change which store is
authoritative.

Agent integration uses the Model Context Protocol (MCP). Central-server
authentication uses OAuth 2.0 and OpenID Connect (OIDC).
