# Maintaining the latest release

`latest` is a moving Git tag used by the installer, including for alpha releases.
It points to the **same Git object** as the selected numbered release tag.
The installer resolves that numbered tag before downloading assets; there is no
duplicate `latest` release or second copy of its binaries.

After publishing and verifying a numbered release, update the alias. For example:

```bash
git fetch origin --tags
previous=$(git ls-remote origin refs/tags/latest | awk '{print $1}')
target=$(git rev-parse refs/tags/v0.0.303)
git update-ref refs/tags/latest "$target"
git push --force-with-lease="refs/tags/latest:$previous" \
  origin refs/tags/latest:refs/tags/latest
```

Substitute the new numbered tag when publishing a subsequent release. Preserve
annotated tag objects: do not peel the target to a commit or create a separate
annotation for `latest`. Never move an existing numbered release tag.

Check that the installer without `SKIG_VERSION` downloads and reports the
intended release, then update the README and Wiki release information. Existing
project pins and running servers still require their explicit upgrade process.
