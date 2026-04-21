import unittest
from cli import normalize_time, looks_like_event_line


class TestParsingFunctions(unittest.TestCase):

    def test_normalize_time_valid(self):
        self.assertEqual(normalize_time("1234"), "12:34")

    def test_normalize_time_empty(self):
        self.assertEqual(normalize_time("////"), "")
        self.assertEqual(normalize_time(""), "")

    def test_looks_like_event_line_valid(self):
        parts = ["1234", "XRA", "1200", "1230", "1300"]
        self.assertTrue(looks_like_event_line(parts))

    def test_looks_like_event_line_invalid(self):
        parts = ["abcd", "123", "1200"]
        self.assertFalse(looks_like_event_line(parts))


if __name__ == "__main__":
    unittest.main()
