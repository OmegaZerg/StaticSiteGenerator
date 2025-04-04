import unittest

from htmlnode import HTMLNode, LeafNode

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
        node = HTMLNode("h1", "This is a test heading.",{"href": "https://www.google.com"},None)
        node2 = HTMLNode("h1", "This is a test heading.",{"href": "https://www.google.com"},None)
        self.assertEqual(node, node2)
    def test_props_to_html(self):
        node = HTMLNode("h1", "This is a test heading.",{"href": "https://www.google.com", "target": "_blank"},None)
        node2 = HTMLNode("h1", "This is a test heading.",{"href": "https://www.google.com"},None)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        self.assertEqual(node2.props_to_html(), " href=\"https://www.google.com\"")

    def test_repr(self):
        node = HTMLNode("h1", "This is a test heading.",{"href": "https://www.google.com", "target": "_blank"},None)
        node2 = HTMLNode("p", "This is a test paragraph.")
        self.assertEqual(repr(node), "HTMLNode(h1, This is a test heading., None, {'href': 'https://www.google.com', 'target': '_blank'})")
        self.assertEqual(repr(node2), "HTMLNode(p, This is a test paragraph., None, None)")

class TestLeafNode(unittest.TestCase):
    def test_leaf_eq(self):
        node = LeafNode("p", "This is a test paragraph.")
        node2 = LeafNode("p", "This is a test paragraph.")
        self.assertEqual(node, node2)

    def test_leaf_eq1(self):
        node = LeafNode("p", "This is a test paragraph.", {'href': 'https://www.google.com', 'target': '_blank'})
        node2 = LeafNode("p", "This is a test paragraph.", {'href': 'https://www.google.com', 'target': '_blank'})
        self.assertEqual(node, node2)

    def test_leaf_eq2(self):
        node = LeafNode("p", "This is a test paragraph.", {'href': 'https://www.google.com' })
        node2 = LeafNode("p", "This is a test paragraph.", {'href': 'https://www.google.com'})
        self.assertEqual(node, node2)

    def test_leaf_repr(self):
        node = LeafNode("h1", "This is a test heading.",{"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode("p", "This is a test paragraph.")
        self.assertEqual(repr(node), "LeafNode(h1, This is a test heading., {'href': 'https://www.google.com', 'target': '_blank'})")
        self.assertEqual(repr(node2), "LeafNode(p, This is a test paragraph., None)")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "Hello, world!")
        self.assertEqual(node.to_html(), "<code>Hello, world!</code>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")  

    def test_leaf_to_html_value_none(self):
        node = LeafNode("p", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            node.to_html() 

        
if __name__ == "__main__":
    unittest.main()