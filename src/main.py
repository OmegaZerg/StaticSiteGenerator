from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        working_list = node.text.split(delimiter)
        if len(working_list) == 1:
            new_nodes.append(node)
            continue
        if len(working_list) % 2 == 0:
            raise ValueError(f"Closing delimiter not found for {delimiter}; i.e. there is markdown with a start but no end")
        for index, item in enumerate(working_list):
            if index % 2 == 0:
                if item:
                    new_nodes.append(TextNode(item, TextType.NORMAL))
            else:
                new_nodes.append(TextNode(item, text_type))
                
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text

        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
                
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining_text = node.text

        for link_text, image_url in links:
            image_markdown = f"[{link_text}]({image_url})"
            parts = remaining_text.split(image_markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, image_url))
            
            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
                
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\((https?:\/\/[^\(\)\s]+)\)", text)
        
def text_to_textnodes(text):
    initial_nodes = [TextNode(text, TextType.NORMAL)]
    new_nodes = split_nodes_delimiter(initial_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def main():
    testing = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(testing)
    print(repr(testing))

main()
