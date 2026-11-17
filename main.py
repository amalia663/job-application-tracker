"""Job Application Tracker."""

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

DATA_FILE = Path("applications.json")
STATUSES = ("applied", "interview", "offer", "rejected")


@dataclass
class Application:
    company: str
    position: str
    status:str = "applied"
    date:str = field(default_factory=lambda: date.today().isoformat())


def load(path: Path = DATA_FILE) -> list[Application]:
    if not path.exists():
        return []
    return [Application(**item) for item in json.loads(path.read_text("utf-8"))]


def save(items: list[Application], path: Path = DATA_FILE) -> None:
    path.write_text(json.dumps([asdict(i) for i in items], indent=2), "utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Track job applications.")
    sub = parser.add_subparsers(dest="cmd",required=True)
    add = sub.add_parser("add")
    add.add_argument("company")
    add.add_argument("position")
    upd = sub.add_parser("update")
    upd.add_argument("number", type=int)
    upd.add_argument("status", choices=STATUSES)
    sub.add_parser("list")
    args = parser.parse_args(argv)


    items = load()
    if args.cmd == "add":
        items .append(Application(args.company, args.position))
        save(items)
    elif args.cmd == "update":
        if not 1 <= args.number <= len (items):
            parser.error(f"no application #{args.number}")
        items [args.number - 1].status = args.status
        save(items)
    for n, i in enumerate(items, 1):
        print(f"{n}. {i.company} - {i.position} [{i.status}]({i.date})")


if __name__ == " __main__":
    main()