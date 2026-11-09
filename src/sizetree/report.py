"""渲染大小树。"""

from __future__ import annotations

import json

from .human import human_size
from .tree import Node, sorted_children


def _percent(size: int, total: int) -> float:
    return (size / total * 100) if total else 0.0


def _line(size: int, total: int, name: str) -> str:
    return f"{human_size(size):>10}  {_percent(size, total):>5.1f}%  {name}"


def render_tree(
    root: Node,
    depth: int = 2,
    min_size: int = 0,
    sort: str = "size",
) -> str:
    lines = [_line(root.size, root.size, f"{root.name}/")]

    def walk(node: Node, prefix: str, level: int) -> None:
        if level > depth:
            return
        children = [
            child for child in sorted_children(node, sort) if child.size >= min_size
        ]
        for index, child in enumerate(children):
            last = index == len(children) - 1
            connector = "└── " if last else "├── "
            label = f"{child.name}/" if child.is_dir else child.name
            lines.append(f"{prefix}{connector}{_line(child.size, root.size, label)}")
            if child.is_dir and level < depth:
                extension = "    " if last else "│   "
                walk(child, prefix + extension, level + 1)

    walk(root, "", 1)
    return "\n".join(lines)


def _node_payload(node: Node, root_size: int, depth: int, min_size: int, sort: str):
    payload = {
        "name": node.name,
        "path": node.path,
        "size": node.size,
        "human_size": human_size(node.size),
        "percent": round(_percent(node.size, root_size), 1),
        "is_dir": node.is_dir,
    }
    if node.is_dir and depth > 0:
        children = [
            child for child in sorted_children(node, sort) if child.size >= min_size
        ]
        payload["children"] = [
            _node_payload(child, root_size, depth - 1, min_size, sort)
            for child in children
        ]
    else:
        payload["children"] = []
    return payload


def render_json(
    root: Node,
    depth: int = 2,
    min_size: int = 0,
    sort: str = "size",
) -> str:
    return json.dumps(
        _node_payload(root, root.size, depth, min_size, sort),
        ensure_ascii=False,
        indent=2,
    )
