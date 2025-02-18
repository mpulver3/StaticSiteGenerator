from enum import Enum

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
