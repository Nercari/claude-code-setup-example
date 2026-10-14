import io
import tempfile
import unittest
from pathlib import Path

from shelvanta import cli, storage
from shelvanta.items import Item


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

    def test_add_with_notes_saves_notes(self):
        self.run_cli("add", "A-1", "Widget", "--notes", "fragile")
        self.assertEqual(storage.load(self.db)["A-1"].notes, "fragile")


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.db = str(Path(self.dir.name) / "shelf.json")

    def tearDown(self):
        self.dir.cleanup()

    def test_load_missing_file_is_empty(self):
        self.assertEqual(storage.load("/nonexistent/shelf.json"), {})

    def test_notes_round_trip(self):
        storage.add_item(self.db, Item("A-1", "Widget", 1, notes="keep dry"))
        self.assertEqual(storage.load(self.db)["A-1"].notes, "keep dry")

    def test_old_rows_without_notes_load_as_empty(self):
        Path(self.db).write_text(
            '{"A-1": {"sku": "A-1", "name": "Widget", "qty": 2, "location": "unsorted"}}',
            encoding="utf-8",
        )
        self.assertEqual(storage.load(self.db)["A-1"].notes, "")

    def test_readd_without_notes_keeps_existing_notes(self):
        storage.add_item(self.db, Item("A-1", "Widget", 1, notes="keep dry"))
        storage.add_item(self.db, Item("A-1", "Widget", 1))
        self.assertEqual(storage.load(self.db)["A-1"].notes, "keep dry")


if __name__ == "__main__":
    unittest.main()
