"""扫描目录并构建大小树。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Node:
    path: str
    name: str
    size: int
    is_dir: bool
    children: list["Node"]


def scan(path: str | Path, name: str | None = None) -> Node:
    target = Path(path)
    children: list[Node] = []
    total = 0

    try:
        entries = list(os.scandir(target))
    except OSError:
        entries = []

    for entry in entries:
        try:
            if entry.is_symlink():
                continue
            if entry.is_dir(follow_symlinks=False):
                child = scan(entry.path)
                children.append(child)
                total += child.size
            elif entry.is_file(follow_symlinks=False):
                stat = entry.stat(follow_symlinks=False)
                children.append(
                    Node(entry.path, entry.name, stat.st_size, False, [])
                )
                total += stat.st_size
        except OSError:
            continue

    display_name = name if name is not None else (target.name or str(target))
    return Node(str(target), display_name, total, True, children)


def sorted_children(node: Node, sort: str = "size") -> list[Node]:
    if sort == "name":
        return sorted(node.children, key=lambda child: child.name.lower())
    return sorted(node.children, key=lambda child: (-child.size, child.name.lower()))
