"""Command line entry point: python -m shelvanta.cli <command>."""
import argparse
import sys

from . import storage
from .items import Item

DEFAULT_DB = "shelf.json"


def build_parser():
    p = argparse.ArgumentParser(prog="shelvanta")
    p.add_argument("--db", default=DEFAULT_DB)
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add", help="add stock for an item")
    a.add_argument("sku")
    a.add_argument("name")
    a.add_argument("--qty", type=int, default=1)
    a.add_argument("--location", default="unsorted")
    r = sub.add_parser("remove", help="remove stock")
    r.add_argument("sku")
    r.add_argument("--qty", type=int, default=1)
    sub.add_parser("list", help="list all items")
    sub.add_parser("count", help="print how many items are stored")
    return p


def main(argv=None, out=sys.stdout):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "add":
            item = storage.add_item(args.db, Item(args.sku, args.name, args.qty, args.location))
            print(f"{item.sku}: {item.qty} in stock", file=out)
        elif args.command == "remove":
            item = storage.remove_qty(args.db, args.sku, args.qty)
            print(f"{item.sku}: {item.qty} in stock", file=out)
        elif args.command == "count":
            print(len(storage.load(args.db)), file=out)
        else:
            for sku, item in sorted(storage.load(args.db).items()):
                print(f"{sku}\t{item.name}\t{item.qty}\t{item.location}", file=out)
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
