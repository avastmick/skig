# Git workflow

Use this mode to keep project knowledge under version control alongside your
code. Git shares the records; no central SKIG server is needed.

## Set up a project

Inside your own Git repository, run:

```bash
skig init
skig install
```

`skig init` creates the project's SKIG metadata. `skig install` adds Git hooks
and agent skills. Review and commit the generated configuration and tracked
`.skig/` records. Keep the SQLite cache and runtime files ignored.

For a project already using SKIG, clone it normally, install its pinned binary
version, then run `skig install` to set up your local hooks and skills.

## Record intent and plan work

```bash
skig req add --category CLI --title "Display command help" \
  --description "Show usage and available commands when invoked with --help."
skig req query
skig task create --type task --title "Implement command help" \
  --description "Add command help and tests for the documented usage."
skig task available
```

Use the IDs returned by SKIG in later commands. For example, replace the
placeholder values below with your actual requirement and task IDs:

```bash
skig req link-task REQUIREMENT_ID TASK_ID
skig task start TASK_ID
```

## Verify and share

After implementing the change, link its evidence. Replace the IDs and file paths
below with values from your project:

```bash
skig req link REQUIREMENT_ID --code src/cli.rs
skig req link REQUIREMENT_ID --test tests/cli.rs
skig verify --level 3
skig task close TASK_ID --message "Implemented and verified"
```

Validation levels are cumulative: 1 checks schema, 2 adds semantics, 3 adds
traceability, and 4 adds governance. `skig verify` runs all four by default.

Review and commit the code, tests and SKIG records through the installed hooks.
Push and review changes using your normal Git workflow. JSON and NDJSON records
preserve project knowledge; SQLite is a disposable query cache.

Use `skig <command> --help` for options and lifecycle rules for your installed
version.
