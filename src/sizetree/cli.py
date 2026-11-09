"""命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .human import parse_size
from .report import render_json, render_tree
from .tree import scan


def _non_negative_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("必须是整数") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("必须是非负整数")
    return value


def _size(raw: str) -> int:
    try:
        return parse_size(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sizetree",
        description="以树状结构展示目录占用，按大小排序。",
    )
    parser.add_argument("path", nargs="?", default=".", help="目录路径（默认当前目录）")
    parser.add_argument(
        "--depth", type=_non_negative_int, default=2, metavar="N", help="展开层数（默认 2）"
    )
    parser.add_argument(
        "--min-size", type=_size, default=0, metavar="SIZE", help="只显示不小于该大小的条目"
    )
    parser.add_argument(
        "--sort", choices=("size", "name"), default="size", help="排序方式"
    )
    parser.add_argument(
        "-f", "--format", choices=("tree", "json"), default="tree", help="输出格式"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    target = Path(args.path).expanduser()
    if not target.exists():
        print(f"sizetree: 路径不存在：{args.path}", file=sys.stderr)
        return 2
    if not target.is_dir():
        print(f"sizetree: 不是目录：{args.path}", file=sys.stderr)
        return 2

    root = scan(target)
    if args.format == "json":
        print(render_json(root, args.depth, args.min_size, args.sort))
    else:
        print(render_tree(root, args.depth, args.min_size, args.sort))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
