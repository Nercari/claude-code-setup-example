import json
import subprocess
import sys
import unittest
from pathlib import Path

HOOK = Path(__file__).with_name("protect_paths.py")


def run_hook(payload, raw=None):
    data = raw if raw is not None else json.dumps(payload)
    return subprocess.run([sys.executable, str(HOOK)], input=data, capture_output=True, text=True)


def edit(path, tool="Edit"):
    return {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {"file_path": path}}


class ProtectPathsTests(unittest.TestCase):
    def assertBlocked(self, path, tool="Edit"):
        r = run_hook(edit(path, tool))
        self.assertEqual(r.returncode, 2, path)
        self.assertIn("Blocked", r.stderr)

    def assertAllowed(self, path):
        self.assertEqual(run_hook(edit(path)).returncode, 0, path)

    def test_blocks_migrations(self):
        self.assertBlocked("/work/tidyshelf/migrations/001_init.sql")
        self.assertBlocked("migrations/002_new.sql", "Write")

    def test_blocks_env_files(self):
        self.assertBlocked("/work/tidyshelf/.env")
        self.assertBlocked("/work/tidyshelf/.env.production")

    def test_blocks_windows_separators(self):
        self.assertBlocked("C:\\work\\tidyshelf\\migrations\\001_init.sql")

    def test_allows_normal_files(self):
        self.assertAllowed("/work/tidyshelf/tidyshelf/cli.py")
        self.assertAllowed("/work/tidyshelf/tests/test_cli.py")

    def test_allows_env_example(self):
        self.assertAllowed("/work/tidyshelf/.env.example")

    def test_similar_names_not_blocked(self):
        self.assertAllowed("/work/tidyshelf/migrations_notes.md")
        self.assertAllowed("/work/tidyshelf/environment.py")

    def test_fails_open_on_garbage(self):
        self.assertEqual(run_hook(None, raw="not json").returncode, 0)
        self.assertEqual(run_hook({"tool_input": {}}).returncode, 0)


if __name__ == "__main__":
    unittest.main()
