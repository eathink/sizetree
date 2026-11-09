import unittest

from sizetree.human import human_size, parse_size


class HumanSizeTests(unittest.TestCase):
    def test_human_size(self):
        cases = {
            0: "0 B",
            1023: "1023 B",
            1024: "1.0 KiB",
            1536: "1.5 KiB",
            2 * 1024**2: "2.0 MiB",
            3 * 1024**3: "3.0 GiB",
        }
        for size, expected in cases.items():
            with self.subTest(size=size):
                self.assertEqual(human_size(size), expected)


class ParseSizeTests(unittest.TestCase):
    def test_units(self):
        cases = {
            "10": 10,
            "10B": 10,
            "10K": 10 * 1024,
            "10KiB": 10 * 1024,
            "1.5M": int(1.5 * 1024**2),
            "2G": 2 * 1024**3,
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(parse_size(raw), expected)

    def test_invalid(self):
        for raw in ("", "abc", "-5", "1X"):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    parse_size(raw)


if __name__ == "__main__":
    unittest.main()
