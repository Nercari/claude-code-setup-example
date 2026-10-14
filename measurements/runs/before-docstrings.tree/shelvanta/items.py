"""Item model and validation."""
from dataclasses import dataclass, asdict


@dataclass
class Item:
    sku: str
    name: str
    qty: int = 0
    location: str = "unsorted"

    def to_dict(self):
        """Return the item's fields as a plain dict."""
        return asdict(self)


def validate(item: Item) -> None:
    """Raise ValueError if the item's sku, name, or qty is invalid."""
    if not item.sku or " " in item.sku:
        raise ValueError("sku must be non-empty and contain no spaces")
    if not item.name.strip():
        raise ValueError("name must not be empty")
    if item.qty < 0:
        raise ValueError("qty must not be negative")
