import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)
    def test_eq1(self):
        node = HTMLNode("p", "This is a test paragraph.")
        node2 = HTMLNode("p", "This is a test paragraph.")
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = HTMLNode("h1", "This is a test heading.",None,{"href": "https://www.google.com"})
        node2 = HTMLNode("h1", "This is a test heading.",None,{"href": "https://www.google.com"})
        self.assertEqual(node, node2)
    def test_props_to_html(self):
        node = HTMLNode("h1", "This is a test heading.",None,{"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("h1", "This is a test heading.",None,{"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        self.assertEqual(node2.props_to_html(), " href=\"https://www.google.com\"")

    def test_repr(self):
        node = HTMLNode("h1", "This is a test heading.",None,{"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("p", "This is a test paragraph.")
        self.assertEqual(repr(node), "HTMLNode(h1, This is a test heading., None, {'href': 'https://www.google.com', 'target': '_blank'})")
        self.assertEqual(repr(node2), "HTMLNode(p, This is a test paragraph., None, None)")

        
if __name__ == "__main__":
    unittest.main()