import unittest
from textnode import TextNode, TextType
from main import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

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

class TestTextNodeSplitImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_image1(self):
        node = TextNode(
        "![test beginning](https://i.imgur.com/zjjcJKZ.png) plus this image: ![test_end](https://i.imgur.com/3elNhQu.png)",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("test beginning", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" plus this image: ", TextType.NORMAL),
                TextNode(
                    "test_end", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_image2(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.NORMAL,
        )
        node2 = TextNode(
        "This is a second node with an ![image2](https://i.imgur.com/ABC123.png) and another ![second image2](https://i.imgur.com/ZYX456.png)",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is a second node with an ", TextType.NORMAL),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/ABC123.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image2", TextType.IMAGE, "https://i.imgur.com/ZYX456.png"
                ),
            ],
            new_nodes,
        )
    def test_split_image_no_image(self):
        node = TextNode(
        "This is just a really long string with nothing of value, no images, or links or any cool stuff",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just a really long string with nothing of value, no images, or links or any cool stuff", TextType.NORMAL),
            ],
            new_nodes,
        )
    def test_split_image_only_image(self):
        node = TextNode(
        "![test beginning](https://i.imgur.com/zjjcJKZ.png)",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("test beginning", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

class TestTextNodeSplitLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
        "This is text with a [link](https://example.com) in it.",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "Here's [one](https://one.com) and [two](https://two.com) links.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here's ", TextType.NORMAL),
                TextNode("one", TextType.LINK, "https://one.com"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("two", TextType.LINK, "https://two.com"),
                TextNode(" links.", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_only_link(self):
        node = TextNode(
        "[link](https://example.com)",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_image_no_link(self):
        node = TextNode(
        "This is just a really long string with nothing of value, no images, or links or any cool stuff",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is just a really long string with nothing of value, no images, or links or any cool stuff", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_link_multiple_node(self):
        node = TextNode(
        "This is text with a [link](https://example.com) in it.",
        TextType.NORMAL,
        )
        node2 = TextNode(
        "This is just a really long string with nothing of value, no images, or links or any cool stuff",
        TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it.", TextType.NORMAL),
                TextNode("This is just a really long string with nothing of value, no images, or links or any cool stuff", TextType.NORMAL),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()