import re
from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType

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
    children = []
    # Match any inline markdown token: **bold**, _italic_, `code`
    pattern = r"(\*\*(.+?)\*\*|`(.+?)`|_(.+?)_)"
    matches = re.finditer(pattern, text)

    last_index = 0  # Track end of last match
    for match in matches:
        # Add plain text before this match (if any)
        start, end = match.span()
        plain_text = text[last_index:start]
        if plain_text:
            children.append(TextNode(plain_text, TextType.NORMAL))
        # Process the current match
        if match.group(2):  # Bold (**bold**)
            children.append(HTMLNode("b", match.group(2)))
        elif match.group(3):  # Code (`code`)
            children.append(HTMLNode("code", match.group(3)))
        elif match.group(4):  # Italic (_italic_)
            children.append(HTMLNode("i", match.group(4)))
        
        # Update the last index to track the end of the current match
        last_index = end

        # Add remaining plain text after the last match as a TextNode
        if last_index < len(text):
            remaining_text = text[last_index:]
            children.append(TextNode(remaining_text, TextType.NORMAL))
        
        return children
    
    
def markdown_to_html_node(markdown):
    clean_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in clean_blocks:
        block_type = block_to_block_type(block)  # Determine type of block
        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            html_nodes.append(HTMLNode("p", children))
        elif block_type == BlockType.HEADING:
            children = text_to_children(block)
            html_nodes.append(HTMLNode(determine_heading(block), children))
        # Code Blocks (special handling)    
        elif block_type == BlockType.CODE:
            text_node = TextNode(block, TextType.NORMAL)  # No inline parsing - plain text
            code_node = HTMLNode("code", [text_node])
            html_nodes.append(HTMLNode("pre", [code_node]))  # Wrap code in <pre>
        # Quote Blocks
        elif block_type == BlockType.QUOTE:
            children = text_to_children(block)
            html_nodes.append(HTMLNode("blockquote", children))
        # Unordered Lists
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.split("\n")  # Split into individual list items
            li_nodes = [HTMLNode("li", [TextNode(item.strip(), TextType.NORMAL)]) for item in list_items]
            html_nodes.append(HTMLNode("ul", li_nodes))
        # Ordered Lists
        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.split("\n")  # Split into individual list items
            li_nodes = [HTMLNode("li", [TextNode(item.strip(), TextType.NORMAL)]) for item in list_items]
            html_nodes.append(HTMLNode("ol", li_nodes))

    #everything goes inside parent <div>
    return HTMLNode("div", html_nodes)