import re
from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType

#We only allow specific HTML "blocks" to be created, using what is setup within the BlockType Enum.
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

#Function that takes a raw markdown string (full document), as input and returns a list of "block" strings. 
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
    
#Helper function to determine the type of heading and return the appropriate HTML heading tag.
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

#Helper function that takes a string of text and returns a list of HTMLNodes that represent the inline markdown.        
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
            #children.append(HTMLNode("b", match.group(2)))
            children.append(HTMLNode("b", [TextNode(match.group(2), TextType.NORMAL)]))
        elif match.group(3):  # Code (`code`)
            #children.append(HTMLNode("code", match.group(3)))
            children.append(HTMLNode("code", [TextNode(match.group(3), TextType.NORMAL)]))
        elif match.group(4):  # Italic (_italic_)
            #children.append(HTMLNode("i", match.group(4)))
            children.append(HTMLNode("i", [TextNode(match.group(4), TextType.NORMAL)]))
        
        # Update the last index to track the end of the current match
        last_index = end

    # Add remaining plain text after the last match as a TextNode
    if last_index < len(text):
        remaining_text = text[last_index:]
        children.append(TextNode(remaining_text, TextType.NORMAL))
    
    return children
    
#Function that converts a full markdown document into a single parent HTMLNode. This parent HTMLNode should contain multiple child HTMLNode objects which represent nested elements.    
def markdown_to_html_node(markdown):
    clean_blocks = markdown_to_blocks(markdown)
    print(f"clean blocks: {clean_blocks}")
    html_nodes = []
    for block in clean_blocks:
        block_type = block_to_block_type(block)  # Determine type of block
        print(f"block type: {block_type}")
        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            print(f"text to chidlren: {children}")
            html_nodes.append(HTMLNode("p", None, None, children))
        elif block_type == BlockType.HEADING:
            children = text_to_children(block)
            html_nodes.append(HTMLNode(determine_heading(block), None, None, children))
        # Code Blocks (special handling)    
        elif block_type == BlockType.CODE:
            text_node = TextNode(block, TextType.NORMAL)  # No inline parsing - plain text
            code_node = HTMLNode("code", None, None, [text_node])
            html_nodes.append(HTMLNode("pre", None, None, [code_node]))  # Wrap code in <pre>
        # Quote Blocks
        elif block_type == BlockType.QUOTE:
            children = text_to_children(block)
            html_nodes.append(HTMLNode("blockquote", None, None, children))
        # Unordered Lists
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.split("\n")  # Split into individual list items
            li_nodes = [HTMLNode("li", None, None, [TextNode(item.strip(), TextType.NORMAL)]) for item in list_items]
            html_nodes.append(HTMLNode("ul", None, None, li_nodes))
        # Ordered Lists
        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.split("\n")  # Split into individual list items
            li_nodes = [HTMLNode("li", None, None, [TextNode(item.strip(), TextType.NORMAL)]) for item in list_items]
            html_nodes.append(HTMLNode("ol", None, None, li_nodes))
        print(f"html nodes: {html_nodes}")
    #everything goes inside parent <div>
    return HTMLNode("div", None, None, html_nodes)