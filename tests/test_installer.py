"""Exercise installation and failure preservation without downloading executables."""

import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


INSTALLER = Path(__file__).resolve().parents[1] / "scripts/install.sh"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skig-installer-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.assets = self.root / "assets"
        self.bin = self.root / "tools"
        self.dest = self.root / "install with spaces"
        for directory in (self.assets, self.bin, self.dest):
            directory.mkdir()
        self.cli = self.assets / "skig-linux-x86_64"
        self.cli.write_text('#!/bin/bash\nprintf "skig 3.0.2\\n"\n')
        (self.assets / "skig-dispatcher-linux-x86_64").write_text(
            '#!/bin/bash\nexec "$(dirname "$0")/skig-v3.0.2" "$@"\n'
        )
        self.manifest()
        self.write_tool("uname", '#!/bin/bash\ncase "$1" in -s) echo Linux;; -m) echo x86_64;; esac\n')
        self.write_tool("curl", '''#!/usr/bin/env python3
import os, pathlib, shutil, sys
args = sys.argv[1:]
url = next(a for a in args if a.startswith('https://'))
with open(os.environ['REQUEST_LOG'], 'a') as log:
    log.write(url + '\\n')
if url.endswith('/latest'):
    print('https://github.com/avastmick/skig/releases/tag/v3.0.2', end='')
else:
    name = url.rsplit('/', 1)[1]
    if os.environ.get('FAIL_ASSET') == name:
        sys.exit(22)
    shutil.copyfile(pathlib.Path(os.environ['ASSETS']) / name,
                  args[args.index('--output') + 1])
''')
        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}",
                        SKIG_INSTALL_DIR=str(self.dest), SKIG_VERSION="3.0.2",
                        ASSETS=str(self.assets), REQUEST_LOG=str(self.root / "requests"))
        self.old = self.dest / "skig"
        self.old.write_text("old dispatcher\n")
        (self.dest / "skig-v2.0.0").write_text("retained old version\n")

    def write_tool(self, name, content):
        path = self.bin / name
        path.write_text(content)
        path.chmod(0o755)

    def manifest(self):
        (self.assets / "SHA256SUMS").write_text("".join(
            f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
            for p in sorted(self.assets.glob("skig-*"))))

    def run_install(self, **environment):
        return subprocess.run(["bash", str(INSTALLER)], env=self.env | environment,
                              capture_output=True, text=True, cwd=self.root)

    def assert_preserved(self, result):
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.old.read_text(), "old dispatcher\n")
        self.assertEqual((self.dest / "skig-v2.0.0").read_text(), "retained old version\n")
        self.assertFalse(list(self.dest.glob(".skig-*")))

    def test_install_and_idempotent_reinstall(self):
        for _ in range(2):
            result = self.run_install()
            self.assertEqual(result.returncode, 0, result.stderr)
        output = subprocess.check_output([str(self.old), "--version"], text=True)
        self.assertEqual(output, "skig 3.0.2\n")
        self.assertTrue((self.dest / "skig-v2.0.0").exists())
        self.assertFalse(list(self.dest.glob(".skig-*")))

    def test_latest_resolved_to_fixed_tag(self):
        result = self.run_install(SKIG_VERSION="latest")
        self.assertEqual(result.returncode, 0, result.stderr)
        requests = (self.root / "requests").read_text().splitlines()
        self.assertTrue(requests[0].endswith('/latest'))
        self.assertEqual(len(requests), 4)
        self.assertTrue(all('/download/v3.0.2/' in url for url in requests[1:]))

    def test_v_prefix(self):
        result = self.run_install(SKIG_VERSION="v3.0.2")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_failed_download(self):
        self.assert_preserved(self.run_install(FAIL_ASSET="skig-dispatcher-linux-x86_64"))

    def test_corrupt_cli_is_not_executed(self):
        marker = self.root / "executed"
        self.cli.write_text(f'#!/bin/bash\ntouch "{marker}"\n')
        self.assert_preserved(self.run_install())
        self.assertFalse(marker.exists())
        self.assertFalse((self.dest / "skig-v3.0.2").exists())

    def test_missing_and_duplicate_checksums(self):
        manifest = self.assets / "SHA256SUMS"
        original = manifest.read_text()
        for content in ("", original + original):
            manifest.write_text(content)
            self.assert_preserved(self.run_install())

    def test_wrong_cli_version(self):
        self.cli.write_text('#!/bin/bash\necho "skig 9.9.9"\n')
        self.manifest()
        self.assert_preserved(self.run_install())

    def test_broken_dispatcher(self):
        (self.assets / "skig-dispatcher-linux-x86_64").write_text('#!/bin/bash\nexit 1\n')
        self.manifest()
        self.assert_preserved(self.run_install())
        self.assertFalse((self.dest / "skig-v3.0.2").exists())

    def test_existing_version_conflict(self):
        target = self.dest / "skig-v3.0.2"
        target.write_text("different content\n")
        target.chmod(0o755)
        self.assert_preserved(self.run_install())
        self.assertEqual(target.read_text(), "different content\n")

    def test_unsupported_platform(self):
        self.write_tool("uname", '#!/bin/bash\necho Darwin\n')
        self.assert_preserved(self.run_install())
        self.assertFalse((self.root / "requests").exists())

    def test_invalid_version(self):
        self.assert_preserved(self.run_install(SKIG_VERSION="../bad"))
        self.assertFalse((self.root / "requests").exists())


if __name__ == "__main__":
    unittest.main()
