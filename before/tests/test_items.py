import unittest

from tidyshelf.items import Item, validate


class ValidateTests(unittest.TestCase):
    def test_ok(self):
        validate(Item("A-1", "Widget", 3))

    def test_space_in_sku(self):
        with self.assertRaises(ValueError):
            validate(Item("A 1", "Widget"))

    def test_negative_qty(self):
        with self.assertRaises(ValueError):
            validate(Item("A-1", "Widget", -1))

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            validate(Item("A-1", "  "))


if __name__ == "__main__":
    unittest.main()
