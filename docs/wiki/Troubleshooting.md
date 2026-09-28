# Troubleshooting

## `skig` is not found

Ensure the installation directory is on your shell's path:

```bash
export PATH="$HOME/.local/bin:$PATH"
command -v skig
skig --version
```

Add the export to your shell startup file if it fixes the problem. An agent
client may need restarting to inherit the updated environment.

## Download verification fails

Stop the installation. Download the binaries and `SHA256SUMS` again from the
same release into an empty directory. Both CLI assets must report `OK` before
installation. Include the release version and asset name in a bug report if
verification still fails.

## The project requests another version

The dispatcher follows the project's toolchain pin. Install the matching release
as `skig-vX.Y.Z` alongside the dispatcher. Keep other versions required by your
projects; do not edit the project's pin just to suppress the error.

## Server login succeeds but access fails

Run `skig auth status` from the configured project. Confirm with the administrator
that your identity has access to the selected graph and that the endpoint and
registration are correct. An identity-provider account alone grants no graph
access. Connection failures require restoring server access, not switching modes.

## Validation fails

Run `skig verify` and read the reported IDs and diagnostics. Correct the records
or referenced files through the appropriate SKIG commands. Use
`skig <command> --help` for your installed version's options.

## Report a problem

Open a [bug report](https://github.com/avastmick/skig/issues/new?template=bug-report.yml)
with your version, Linux distribution or WSL environment, usage mode, reproduction
steps, and expected and actual behaviour. Include relevant error output after
removing credentials and private project data.
