import unittest

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



if __name__ == "__main__":
    unittest.main()
