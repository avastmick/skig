# Agent integration

SKIG provides project skills and a Model Context Protocol (MCP) interface so
agents can query requirements, find work and record progress.

## Install project skills

Inside an initialised or server-configured project, run:

```bash
skig install
```

Skills use the shared `.agents/skills/` discovery path. Check that your agent
tool reads project instructions and skills from that location.

## Configure MCP

Generate the project's MCP configuration:

```bash
skig mcp init
```

Review the generated `.mcp.json` and load it in your MCP-compatible client.
Clients with their own configuration format should launch `skig mcp serve`
using stdio transport, with the working directory set to the project and
`skig` available on `PATH`.

The MCP process uses the project's selected graph and pinned toolchain. For
server-backed projects, sign in with `skig auth login` first. MCP calls enforce
the same server access grants as CLI commands; a server outage does not create
a local graph.

Review proposed changes using your usual project workflow. Agent access does
not bypass SKIG validation or lifecycle rules.
