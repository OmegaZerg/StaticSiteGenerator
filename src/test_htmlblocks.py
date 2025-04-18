import unittest
from htmlblocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node, text_to_children
from textnode import TextNode, TextType
from htmlnode import HTMLNode

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
        This is **bolded** paragraph



        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line



        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        md = "# THIS IS A HEADING"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type1(self):
        md = "###### This is a baby heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type2(self):
        md = "``` This is a\n code block```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type3(self):
        md = ">This is a quote"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type4(self):
        md = ">This is a quote with\n>multiple lines\n>because reasons."
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type5(self):
        md = "- This is a list\n- with items"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_code_heading(self):
        md = "```###### This is a baby heading```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_Invalid1(self):
        md = "```This is a baby heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid2(self):
        md = ">This is a quote with\n>multiple lines\nbecause reasons."
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

class TestTextToChildren(unittest.TestCase):
    def test_regular(self):
        md = "This is just plain text with no markdown."

        children = text_to_children(md)
        self.assertEqual(
            children,[
            TextNode("This is just plain text with no markdown.", TextType.NORMAL)
        ],
        )

    def test_adjacent_multiple(self):
        md = "**bold**_italic_`code`"

        children = text_to_children(md)
        self.assertEqual(
            children,[
            HTMLNode("b", None, None, [TextNode("bold", TextType.NORMAL)]),
            HTMLNode("i", None, None, [TextNode("italic", TextType.NORMAL)]),
            HTMLNode("code", None, None, [TextNode("code", TextType.NORMAL)])
        ],
        )

    def test_multiple(self):
        md = "This is **bold** and _italic_ with `code`."

        children = text_to_children(md)
        self.assertEqual(
            children,[
            TextNode("This is ", TextType.NORMAL),
            HTMLNode("b", None, None, [TextNode("bold", TextType.NORMAL)]),
            TextNode(" and ", TextType.NORMAL),
            HTMLNode("i", None, None, [TextNode("italic", TextType.NORMAL)]),
            TextNode(" with ", TextType.NORMAL),
            HTMLNode("code", None, None, [TextNode("code", TextType.NORMAL)]),
            TextNode(".", TextType.NORMAL)
        ],
        )

    def test_unmatched(self):
        md = "This is not **bold and `code"

        children = text_to_children(md)
        self.assertEqual(
            children,[
            TextNode("This is not **bold and `code", TextType.NORMAL)
        ],
        )

class TestMardownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )