import unittest
from create_nodes import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.IMAGE, "Some URL.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "Some URL.com")
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "Some URL.com")
        node2 = TextNode("This is a text node", TextType.LINK, "Some other URL.com")
        self.assertNotEqual(node, node2)
    def test_none(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url, None)
    def test_not_empty(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.url, None)
        self.assertEqual(node2.text, "This is a text node")
        self.assertEqual(node2.url, None)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "Some URL.com")
        node2 = TextNode("This is a text node2", TextType.CODE)
        self.assertEqual(repr(node2), "TextNode(This is a text node2, `Code text`, None)")

class TestTextNodeConversion(unittest.TestCase):
    def test_normal_text(self):
        node = TextNode("This is a normal text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a normal text node")
    def test_bold_text(self):
        node = TextNode("This is BOLD text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is BOLD text")
    def test_italic_text(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
    def test_code_text(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "url.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "url.com"})
    def test_image(self):
        node = TextNode("This is image description text", TextType.IMAGE, "imageURL.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "imageURL.com", "alt": "This is image description text"})
    #Extra tests
    def test_empty_alt_text(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("", TextType.IMAGE, "SomeURL.com")
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Missing alt text for image.")
    def test_empty_url_link(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("A link with no URL", TextType.LINK, "")
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Missing required URL for text type: TextType.LINK")

    def test_invalid_text_type(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("This is image description text", "INVALID", "imageURL.com")
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Text node does not contain a valid text type")
    def test_none_text_type(self):
        with self.assertRaises(ValueError) as context:
            node = TextNode("This is image description text", None, "imageURL.com")
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Text node does not contain a valid text type")


if __name__ == "__main__":
    unittest.main()
