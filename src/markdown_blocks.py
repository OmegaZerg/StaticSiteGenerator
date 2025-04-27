import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from create_nodes import text_node_to_html_node, text_to_textnodes

#We only allow specific HTML "blocks" to be created, using what is setup within the BlockType Enum.
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


#Function that takes a raw markdown string (full document), as input and returns a list of "block" strings by removing extra new lines and/or newlines with whitespace after.
def markdown_to_blocks(markdown_document):
    blocks = markdown_document.split("\n\n")
    clean_blocks = []
    for block in blocks:
        if block != "\n" and block != "":
            clean_blocks.append(re.sub(r'\n\s+', '\n', block.strip()))
    return clean_blocks

#Helper function to determine if a line of markdown is an ordered list.
def is_ordered_list(lines):
    for i, line in enumerate(lines):
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            return False
    return True

#Function that takes a single block of markdown text as input and returns the BlockType representing the type of block it is.
def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### " )):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
#Function that takes a raw markdown document and converts it into a single ParentNode. First we breakdown the document into clean blocks. For each block, create the ParentNode and append to the children list. Finally the children list are wrapped inside a main ParentNode div.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

#Function that takes in a single block of markdown, determines what type of block it is (Paragraph, heading, etc.), then returns the appropriate ParentNode based on the contents.
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

#Helper function that takes string and converts the string into a list of text nodes that represent the original string. Then each TextNode object in the list is converted to a LeafNode (these are all children).
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

#Helper function takes a block of markdown(of type paragraph), and converts it into a single ParentNode with children. 
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

#Helper function that takes a block of markdown(of type heading), determines what heading level is being used. Then returns the appropriate heading tag with children.
def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

#Helper function that takes a block of markdown(of type code), strips away the code markdown (```), creates a LeafNode, and finally returns the LeafNode that is wrapped inside ParentNode with a 'code' tag, and that is wrapped in another ParentNode with a 'pre' tag.
def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.NORMAL)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

#Helper function that takes a block of markdown(of type ordered list),
def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)