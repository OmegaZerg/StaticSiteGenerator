import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        self.assertEqual(repr(node), "HTMLNode(h1, This is a test heading., [], {'href': 'https://www.google.com', 'target': '_blank'})")
        self.assertEqual(repr(node2), "HTMLNode(p, This is a test paragraph., [], None)")

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
        try:
            LeafNode("p", None, {"href": "https://www.google.com"})
        except ValueError as e:
            assert str(e) == "Value cannot be None"

class TestParentNode(unittest.TestCase):
    def test_to_html_with_no_tag(self):
        try:
            ParentNode("", [LeafNode("span", "child")])
        except ValueError as e:
            assert str(e) == "Tags cannot be None or empty"

    def test_to_html_with_none_tag(self):
        try:
            ParentNode(None, [LeafNode("p", "text")])
        except ValueError as e:
            assert str(e) == "Tags cannot be None or empty"

    def test_to_html_with_no_children(self):
        try:
            ParentNode("div", [])
        except ValueError as e:
            assert str(e) == "Children must be a non-empty list"

    def test_to_html_with_none_children(self):
        try:
            ParentNode("div", None)
        except ValueError as e:
            assert str(e) == "Children must be a non-empty list"

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child content")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child content</span></div>")

    def test_to_html_with_invalid_child(self):
        try:
            ParentNode("div", [1])
        except ValueError as e:
            assert str(e) == "Children must be an HTMLNode object"

    def test_to_html_with_invalid_child2(self):
        try:
            ParentNode("div", [1, "invalid child"])
        except ValueError as e:
            assert str(e) == "Children must be an HTMLNode object"

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild content")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild content</b></span></div>",
        )

    def test_to_html_with_grandchildren2(self):
        grandchild_node2 = LeafNode("b", "grandchild content")
        grandchild_node1 = ParentNode("p", [grandchild_node2])
        child_node = ParentNode("span", [grandchild_node1])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>grandchild content</b></p></span></div>",
        )

    def test_mixed_children(self):
        leaf_one = LeafNode(None, "Text1")
        leaf_two = LeafNode("b", "Bold")
        child_parent = ParentNode("span", [leaf_two])
        parent_node = ParentNode("div", [leaf_one, child_parent])
        expected_html = "<div>Text1<span><b>Bold</b></span></div>"
        assert parent_node.to_html() == expected_html

    def test_props_handling(self):
        props = {"class": "highlight", "id": "main"}
        child_node = LeafNode("p", "content")
        parent_node = ParentNode("div", [child_node], props)
        assert parent_node.props == props

    def test_extremely_deep_nesting(self):
        deep_node = LeafNode("span", "text")
        for _ in range(50):
            deep_node = ParentNode("div", [deep_node])
        assert "span" in deep_node.to_html()

    def test_many_children(self):
       children = [LeafNode("p", f"text {i}") for i in range(1000)]
       parent_node = ParentNode("div", children)
       output = parent_node.to_html()
       for i in range(1000):
           assert f"<p>text {i}</p>" in output

    def test_props_none(self):
        parent = ParentNode("div", [LeafNode("p", "text")])
        assert parent.props is None

    def test_empty_props(self):
        parent = ParentNode("div", [LeafNode("p", "content")])
        assert parent.to_html() == "<div><p>content</p></div>"

    def test_props(self):
        props = {"class": "highlight", "id": "main"}
        parent = ParentNode("div", [LeafNode("span", "text")], props)
        # Expected output would integrate the props into the tag
        expected_html = '<div class="highlight" id="main"><span>text</span></div>'
        assert parent.to_html() == expected_html

    def test_nested_invalid_child(self):
        try:
            invalid_child = ParentNode("span", [1])
            ParentNode("div", [invalid_child])
        except ValueError as e:
           assert str(e) == "Children must be an HTMLNode object"

    def test_escapted_html(self):
        props = {"data-value": '5"', "custom": "abc&def"}
        parent = ParentNode("div", [LeafNode("p", "text")], props)
        # Expected HTML with properly escaped special characters
        expected_html = '<div data-value="5&quot;" custom="abc&amp;def"><p>text</p></div>'
        assert parent.to_html() == expected_html

    def test_escapted_html1(self):
        props = {"data-title": 'Quotes "inside"', "text": "Some & symbol"}
        parent = ParentNode("div", [LeafNode("p", "content")], props)
        # Expected HTML with properly escaped special characters
        expected_html = '<div data-title="Quotes &quot;inside&quot;" text="Some &amp; symbol"><p>content</p></div>'
        assert parent.to_html() == expected_html
        
    def test_recursive_rendering_with_props(self):
        # Leaf node with text
        grandchild = LeafNode("span", "Grandchild text", props={"class": "grand"})

        # Child node with nested children and their own props
        child = ParentNode(
            "div",
            [grandchild],
            props={"id": "child", "data-type": "nested"}
        )

        # Parent node with child nodes and its own props
        parent = ParentNode(
            "section",
            [child],
            props={"class": "container", "role": "main"}
        )

        expected_html = (
            '<section class="container" role="main">'
            '<div id="child" data-type="nested">'
            '<span class="grand">Grandchild text</span>'
            '</div>'
            '</section>'
        )
        assert parent.to_html() == expected_html

    def test_invalid_props_values(self):
        # Props containing invalid value types
        props = {"class": "main", "custom": None, "count": 5}
        parent = ParentNode("div", [LeafNode("p", "text")], props)

        # Handle only string-convertible props or skip invalid ones
        expected_html = '<div class="main" count="5"><p>text</p></div>'
        assert parent.to_html() == expected_html

if __name__ == "__main__":
    unittest.main()