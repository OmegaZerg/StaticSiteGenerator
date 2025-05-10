import unittest
from generate_pages import extract_title, generate_page

class TestExtractTitle(unittest.TestCase):
    def test_with_title(self):
        md = """
# This is a title for a web page.  

This is a paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is a title for a web page."
        )
    def test_without_title(self):
        md = """
This is a web page without a title/h1.  

This is a paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        try:
            title = extract_title(md)
        except Exception as e:
            assert str(e) == "Error: No title(h1 header) found in provided markdown document"
    def test_with_multiple_title(self):
        md = """
# This is a title for a web page.  
# Another H1??? HOW DARE YOU!
This is a paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
# 3 primary headers in a single page? This is out of control!
- This is a list
- with items
        """
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is a title for a web page."
        )

class TestGeneratePage(unittest.TestCase):
    def test_generate_page1(self):
        generate_page()
