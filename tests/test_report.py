import json
import tempfile
import unittest
from pathlib import Path

from helpers import make_tree
from sizetree.report import render_json, render_tree
from sizetree.tree import scan


class RenderTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        make_tree(self.root)
        self.node = scan(self.root, name="root")

    def test_depth_zero_shows_only_root(self):
        output = render_tree(self.node, depth=0)

        self.assertEqual(len(output.splitlines()), 1)
        self.assertIn("root/", output)
        self.assertIn("100.0%", output)

    def test_depth_one_shows_direct_children(self):
        output = render_tree(self.node, depth=1)

        self.assertEqual(len(output.splitlines()), 3)
        self.assertIn("a.txt", output)
        self.assertIn("dir/", output)
        self.assertNotIn("b.txt", output)

    def test_depth_two_shows_grandchildren(self):
        output = render_tree(self.node, depth=2)

        self.assertIn("b.txt", output)
        self.assertIn("sub/", output)

    def test_min_size_filters(self):
        output = render_tree(self.node, depth=2, min_size=400)

        self.assertIn("dir/", output)
        self.assertNotIn("a.txt", output)
        self.assertNotIn("b.txt", output)

    def test_json_structure(self):
        payload = json.loads(render_json(self.node, depth=1))

        self.assertEqual(payload["name"], "root")
        self.assertEqual(payload["size"], 600)
        self.assertEqual({child["name"] for child in payload["children"]}, {"a.txt", "dir"})
        self.assertTrue(all(child["children"] == [] for child in payload["children"]))

    def test_json_depth_zero(self):
        payload = json.loads(render_json(self.node, depth=0))

        self.assertEqual(payload["children"], [])


if __name__ == "__main__":
    unittest.main()
