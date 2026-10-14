"""JSON-file storage. The file path is passed in, never hard-coded."""
import json
from pathlib import Path

from .items import Item, validate


def load(path):
    p = Path(path)
    if not p.exists():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {sku: Item(**row) for sku, row in data.items()}


def save(path, inventory):
    data = {sku: item.to_dict() for sku, item in sorted(inventory.items())}
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def add_item(path, item: Item):
    validate(item)
    inv = load(path)
    if item.sku in inv:
        inv[item.sku].qty += item.qty
    else:
        inv[item.sku] = item
    save(path, inv)
    return inv[item.sku]


def count_items(path) -> int:
    return len(load(path))


def remove_qty(path, sku, qty):
    inv = load(path)
    if sku not in inv:
        raise KeyError(f"unknown sku: {sku}")
    if qty > inv[sku].qty:
        raise ValueError("not enough stock")
    inv[sku].qty -= qty
    save(path, inv)
    return inv[sku]
