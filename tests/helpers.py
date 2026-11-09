from pathlib import Path


def make_tree(root: Path) -> None:
    (root / "a.txt").write_bytes(b"a" * 100)
    directory = root / "dir"
    directory.mkdir()
    (directory / "b.txt").write_bytes(b"b" * 200)
    sub = directory / "sub"
    sub.mkdir()
    (sub / "c.txt").write_bytes(b"c" * 300)
