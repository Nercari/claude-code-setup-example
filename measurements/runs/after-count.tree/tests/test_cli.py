import io
import tempfile
import unittest
from pathlib import Path

from shelvanta import cli, storage


class CliTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.db = str(Path(self.dir.name) / "shelf.json")

    def tearDown(self):
        self.dir.cleanup()

    def run_cli(self, *argv):
        out = io.StringIO()
        code = cli.main(["--db", self.db, *argv], out=out)
        return code, out.getvalue()

    def test_add_then_list(self):
        self.assertEqual(self.run_cli("add", "A-1", "Widget", "--qty", "4")[0], 0)
        code, text = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("A-1\tWidget\t4", text)

    def test_add_twice_sums(self):
        self.run_cli("add", "A-1", "Widget", "--qty", "2")
        _, text = self.run_cli("add", "A-1", "Widget", "--qty", "3")
        self.assertIn("5 in stock", text)

    def test_remove_too_much_fails(self):
        self.run_cli("add", "A-1", "Widget", "--qty", "1")
        code, _ = self.run_cli("remove", "A-1", "--qty", "5")
        self.assertEqual(code, 1)

    def test_remove_unknown_fails(self):
        self.assertEqual(self.run_cli("remove", "ZZ")[0], 1)

    def test_count_counts_distinct_items(self):
        self.run_cli("add", "A-1", "Widget", "--qty", "2")
        self.run_cli("add", "A-1", "Widget", "--qty", "3")
        self.run_cli("add", "B-2", "Gadget")
        code, text = self.run_cli("count")
        self.assertEqual(code, 0)
        self.assertEqual(text, "2\n")

    def test_count_empty_store_is_zero(self):
        code, text = self.run_cli("count")
        self.assertEqual(code, 0)
        self.assertEqual(text, "0\n")


class StorageTests(unittest.TestCase):
    def test_load_missing_file_is_empty(self):
        self.assertEqual(storage.load("/nonexistent/shelf.json"), {})

    def test_count_items_missing_file_is_zero(self):
        self.assertEqual(storage.count_items("/nonexistent/shelf.json"), 0)


if __name__ == "__main__":
    unittest.main()
