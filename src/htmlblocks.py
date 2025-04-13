import re
from enum import Enum
from htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown_document):
    blocks = markdown_document.split("\n\n")
    clean_blocks = []
    for block in blocks:
        if block != "\n" and block != "":
            clean_blocks.append(re.sub(r'\n\s+', '\n', block.strip()))
    return clean_blocks

def is_ordered_list(lines):
    for i, line in enumerate(lines):
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            return False
    return True

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
    
def determine_heading(heading_block):
    match (heading_block):
        case (heading_block.startswith("# ")):
            return "h1"
        case (heading_block.startswith("## ")):
            return "h2"
        case (heading_block.startswith("### ")):
            return "h3"
        case (heading_block.startswith("#### ")):
            return "h4"
        case (heading_block.startswith("##### ")):
            return "h5"
        case (heading_block.startswith("###### ")):
            return "h6"
        case _:
            raise Exception("invalid heading type")
        
def text_to_children(text):
    pass
    
def markdown_to_html_node(markdown):
    clean_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in clean_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            #block needs to be replaced with text to children function???
            html_nodes.append(HTMLNode("p", block))
        elif block_type == BlockType.HEADING:
            html_nodes.append(HTMLNode(determine_heading(block), block))
        elif block_type == BlockType.CODE:
            html_nodes.append(HTMLNode("code", block))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(HTMLNode("blockquote", block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_nodes.append(HTMLNode("ul", block))
        elif block_type == BlockType.ORDERED_LIST:
            html_nodes.append(HTMLNode("ol", block))