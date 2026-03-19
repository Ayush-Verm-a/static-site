from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    md_blocks = markdown.split("\n\n")
    md_blocks_strip = []
    for block in md_blocks:
        if block != "":
            md_blocks_strip.append(block.strip())

    return md_blocks_strip

def block_to_block_type(block):
    head = ""
    lines = block.split("\n")
    flag = True
    if block.startswith("#"):
        for i in range(6):
            head += "#"
            if block.startswith(head+" "):
                return BlockType.HEADING 
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not(line.startswith(">") or line.startswith("> ")):
                flag = False
        if flag:
            return BlockType.QUOTE
    elif block.startswith("-"):
        for line in lines:
            if not line.startswith("- "):
                flag = False
        if flag:
            return BlockType.UNORDERED_LIST
    elif block.startswith("1"):
        for i in range(1, len(lines)+1):
            if not lines[i-1].startswith(f"{i}. "):
                flag = False
        if flag:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
            

    
