import unittest
from utils import extract_title

class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        md="# Hello  "
        title = extract_title(md)
        self.assertEqual("Hello", title)
    