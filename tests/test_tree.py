import os
import tempfile
import unittest
from pathlib import Path

from helpers import make_tree
from sizetree.tree import scan, sorted_children


class TreeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        make_tree(self.root)

    def test_total_size_and_children(self):
        node = scan(self.root, name="root")

        self.assertEqual(node.size, 600)
        self.assertEqual(
            {child.name: (child.size, child.is_dir) for child in node.children},
            {"a.txt": (100, False), "dir": (500, True)},
        )

    def test_sorted_by_size_desc(self):
        node = scan(self.root)

        children = sorted_children(node)
        self.assertEqual([child.name for child in children], ["dir", "a.txt"])

    def test_sorted_by_name(self):
        node = scan(self.root)

        children = sorted_children(node, "name")
        self.assertEqual([child.name for child in children], ["a.txt", "dir"])

    def test_symlinks_are_skipped(self):
        os.symlink(self.root / "a.txt", self.root / "link.txt")

        node = scan(self.root)

        self.assertEqual(node.size, 600)
        self.assertNotIn("link.txt", [child.name for child in node.children])

    def test_missing_directory_is_empty(self):
        node = scan(self.root / "missing")

        self.assertEqual(node.size, 0)
        self.assertEqual(node.children, [])


if __name__ == "__main__":
    unittest.main()
