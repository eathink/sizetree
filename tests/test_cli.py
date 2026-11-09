import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from helpers import make_tree
from sizetree.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)
        make_tree(self.root)

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_tree_output(self):
        code, out, _ = self.run_cli(str(self.root), "--depth", "2")

        self.assertEqual(code, 0)
        self.assertIn("a.txt", out)
        self.assertIn("sub/", out)

    def test_json_output(self):
        code, out, _ = self.run_cli(str(self.root), "--format", "json")

        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(payload["size"], 600)

    def test_depth_zero(self):
        code, out, _ = self.run_cli(str(self.root), "--depth", "0")

        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().splitlines()), 1)

    def test_min_size(self):
        code, out, _ = self.run_cli(str(self.root), "--min-size", "400")

        self.assertEqual(code, 0)
        self.assertNotIn("a.txt", out)
        self.assertIn("dir/", out)

    def test_missing_path_returns_two(self):
        code, _, err = self.run_cli(str(self.root / "missing"))

        self.assertEqual(code, 2)
        self.assertIn("sizetree:", err)

    def test_file_path_returns_two(self):
        code, _, err = self.run_cli(str(self.root / "a.txt"))

        self.assertEqual(code, 2)
        self.assertIn("不是目录", err)


if __name__ == "__main__":
    unittest.main()
