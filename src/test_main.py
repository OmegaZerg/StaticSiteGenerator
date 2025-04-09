import unittest
from textnode import TextNode, TextType
from main import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images1(self):
        matches = extract_markdown_images(
            "This is text with an ![OMG THIS is an image of something 1337!](https://some_big_dino_dude.com/alakablamoKZ.gif)"
        )
        self.assertListEqual([("OMG THIS is an image of something 1337!", "https://some_big_dino_dude.com/alakablamoKZ.gif")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images3(self):
        matches = extract_markdown_images(
            "![image1](https://link1.com) and ![image2](https://link2.com), but watch out for [not an image](broken link)!"
        )
        self.assertListEqual([('image1', 'https://link1.com'), ('image2', 'https://link2.com')], matches)

class TestMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links1(self):
        matches = extract_markdown_links(
            "This is text with a link [OMG THIS is an image of something 1337!](https://some_big_dino_dude.com/alakablamoKZ.gif)"
        )
        self.assertListEqual([("OMG THIS is an image of something 1337!", "https://some_big_dino_dude.com/alakablamoKZ.gif")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with a link [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links3(self):
        matches = extract_markdown_links(
            "[link1](https://link1.com) and [link2](https://link2.com), but watch out for [not a link](broken link)!"
        )
        self.assertListEqual([('link1', 'https://link1.com'), ('link2', 'https://link2.com')], matches)

    def test_extract_markdown_links4(self):
        matches = extract_markdown_links("A link [to Boot.dev](https://www.boot.dev), an image ![cool pic](https://example.com/image.jpg), and another [to YouTube](https://www.youtube.com)."
        )
        self.assertListEqual([('to Boot.dev', 'https://www.boot.dev'), ('to YouTube', 'https://www.youtube.com')], matches)



class TestTextNodeSplitByDelimiter(unittest.TestCase):
    def test_split_text(self):
        node = TextNode("This is text with an _italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual([
        TextNode("This is text with an ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word", TextType.NORMAL),
], new_nodes)

    def test_split_text1(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.NORMAL
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.NORMAL

    def test_split_text2(self):
        node = TextNode("Text with `code` and more `code blocks` in it", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 5
        assert new_nodes[0].text_type == TextType.NORMAL
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text_type == TextType.NORMAL
        assert new_nodes[3].text_type == TextType.CODE
        assert new_nodes[4].text_type == TextType.NORMAL

    def test_split_text3(self):
        node = TextNode("This has **bold text** in it", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 3
        assert new_nodes[1].text == "bold text"
        assert new_nodes[1].text_type == TextType.BOLD

    def test_split_text4(self):
        node = TextNode("Plain text with no special formatting", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Plain text with no special formatting"
        assert new_nodes[0].text_type == TextType.NORMAL

    def test_split_text5(self):
        node = TextNode("Text with an empty ``", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 2
        assert new_nodes[0].text == "Text with an empty "
        assert new_nodes[1].text == ""
        assert new_nodes[1].text_type == TextType.CODE

    def test_split_text6(self):
        node = TextNode("Already formatted text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Already formatted text"
        assert new_nodes[0].text_type == TextType.BOLD

    def test_split_text7(self):
        node1 = TextNode("First `code` node", TextType.NORMAL)
        node2 = TextNode("Second **bold** node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        assert len(new_nodes) == 4
        assert new_nodes[0].text == "First "
        assert new_nodes[1].text == "code"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " node"
        assert new_nodes[3].text == "Second **bold** node"

    def test_split_text8(self):
        node = TextNode("Text with unbalanced `code", TextType.NORMAL)
        try:
            split_nodes_delimiter([node], "`", TextType.CODE)
            assert False, "Expected ValueError but no exception was raised"
        except ValueError:
            assert True

    def test_split_text8(self):
        node = TextNode("`code block` with normal text `another code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "code block"
        assert new_nodes[0].text_type == TextType.CODE
        assert new_nodes[1].text == " with normal text "
        assert new_nodes[1].text_type == TextType.NORMAL
        assert new_nodes[2].text == "another code"
        assert new_nodes[2].text_type == TextType.CODE

if __name__ == "__main__":
    unittest.main()