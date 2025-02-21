from enum import Enum
from textnode import *
from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

#input multi-line text, then outpus a list of "block strings" (each is separated by a blank line)
def markdown_to_blocks(markdown):
    list_of_strings = markdown.split("\n\n")
    new_list = []
    for s in list_of_strings:
        if s != "":
            new_list.append(s.strip("\n"))
    return new_list

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    block_lines = block.split("\n")
    quote_count = 0
    unordered_count = 0
    ordered_count = 0
    count = 1
    for line in block_lines:
        if line.startswith(">"):
            quote_count += 1
        elif line.startswith(("* ", "- ", "+ ")):
            unordered_count += 1
        elif line.startswith(f"{count}. "):
            ordered_count += 1
        count += 1
    if quote_count == len(block_lines):
        return BlockType.QUOTE
    elif unordered_count == len(block_lines):
        return BlockType.ULIST
    elif ordered_count == len(block_lines):
        return BlockType.OLIST
    elif len(block) >= 6:
        if block.startswith("```") and block.startswith("```", (len(block)-3)):
            return BlockType.CODE
        return BlockType.PARAGRAPH
    else: 
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.OLIST:
            children.append(olist_to_html_node(block))
        elif block_type == BlockType.ULIST:
            children.append(ulist_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        else:
            raise ValueError("invalid block type")
    return ParentNode("div", children, None)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html_node(block):
    if block.startswith("```") and block.endswith("```"):
        text = block[4:-3]
        children = text_to_children(text)
        code = ParentNode("code", children)
        code_list = [code]
        return ParentNode("pre", code_list)
    else:
        raise ValueError("Invalid formatting - code")

def heading_to_html_node(block):
    header_size = 1
    for c in block:
        if c == "#":
            header_size += 1
        else:
            break
    if header_size  >= len(block):
        raise ValueError(f"Invalid formatting - Header")
    text = block[header_size:]
    children = text_to_children(text)
    return ParentNode(f"h{header_size - 1}", children)

def olist_to_html_node(block):
    items = block.split("\n")
    item_list = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        item_list.append(ParentNode("li", children))
    return ParentNode("ol", item_list)

def ulist_to_html_node(block):
    items = block.split("\n")
    item_list = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        item_list.append(ParentNode("li", children))
    return ParentNode("ul", item_list)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if line.startswith(">") != True:
            raise ValueError("Invalid formatting - quote")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
