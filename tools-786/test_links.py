import tempfile
import unittest
from pathlib import Path
from check_links import check


class LinkTests(unittest.TestCase):
    def test_links_and_fragments(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'index.html').write_text('<a href="other.html#fine">ok</a><a href="https://example.org">external</a>')
            (root / 'other.html').write_text('<p id="fine">hello</p>')
            self.assertEqual(check(root), (2, []))
            (root / 'index.html').write_text('<a href="other.html#missing">x</a><a href="gone.html">y</a>')
            _, errors = check(root)
            self.assertEqual(len(errors), 2)
            self.assertTrue(any('fragment' in e for e in errors))
            self.assertTrue(any('missing target' in e for e in errors))

    def test_escape_and_duplicate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'index.html').write_text('<a href="../escape">x</a><p id="a"></p><p id="a"></p>')
            _, errors = check(root)
            self.assertEqual(len(errors), 2)

    def test_empty_directory_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertTrue(check(temp)[1])


if __name__ == '__main__':
    unittest.main()
