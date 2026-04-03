import unittest
from main import extract_title

class TestHTMLNode(unittest.TestCase):
    def test_extract_title(self):
        title = "# Hello World"
        self.assertEqual(extract_title(title), "Hello World")
    
    def test_extract_improper_syntax(self):
        title = "## Hello World"
        title2 = "Hello World"
        title3 = "#Hello World)"
        with self.assertRaises(Exception):
            extract_title(title)
        with self.assertRaises(Exception):
            extract_title(title2)
        with self.assertRaises(Exception):
            extract_title(title3)
        