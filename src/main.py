from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise ValueError("Text node does not contain a valid text type")
    if text_node.text_type in (TextType.LINK, TextType.IMAGE) and not text_node.url:
        raise ValueError(f"Missing required URL for text type: {text_node.text_type}")
    if text_node.text_type == TextType.IMAGE and not text_node.text:
        raise ValueError("Missing alt text for image.")
    match (text_node.text_type):
        case (TextType.NORMAL):
            leaf_node = LeafNode(None, text_node.text)
            return leaf_node
        case (TextType.BOLD):
            leaf_node = LeafNode("b", text_node.text)
            return leaf_node
        case (TextType.ITALIC):
            leaf_node = LeafNode("i", text_node.text)
            return leaf_node
        case (TextType.CODE):
            leaf_node = LeafNode("code", text_node.text)
            return leaf_node
        case (TextType.LINK):
            leaf_node = LeafNode("a", text_node.text, {"href": text_node.url})
            return leaf_node
        case (TextType.IMAGE):
            leaf_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return leaf_node


def main():
    testing = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(testing)
    print(repr(testing))

main()
