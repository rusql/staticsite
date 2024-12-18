import enum as e

class BlockType(e.Enum):
    HEADING1 = "heading 1"
    HEADING2 = "heading 2"
    HEADING3 = "heading 3"
    HEADING4 = "heading 4"
    HEADING5 = "heading 5"
    HEADING6 = "heading 6"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    lines.append("") #add an empty line to the list otherwise we skip the last element
    blocks=[]
    this_line = ""
    for line in lines:
        if line.strip() == "":
            if this_line != "":
                blocks.append(this_line.strip())
                this_line = ""
        else:
            this_line += line+"\n"
    return blocks

def list_items_all_start_with(list, s):
    if len(list) == 0:
        return False
    for item in list:
        if not item.startswith(s):
            return False
    return True

def is_ordered_list(list):
    if len(list) == 0:
        return False
    line_no = 0    
    for item in list:
        line_no += 1
        if not item.startswith(f"{line_no}. "):
            return False
    return True


def block_to_block_type(block):

    if len(block) == 0:
        return BlockType.PARAGRAPH
    
    lines = block.split("\n")
    line_count = len(lines)
    
    if line_count == 0:
        return BlockType.PARAGRAPH
    if lines[0].startswith("```") and lines[line_count-1].endswith("```"):
        return BlockType.CODE
    if list_items_all_start_with(lines, "# "):
        return BlockType.HEADING1
    if list_items_all_start_with(lines,"## "):
        return BlockType.HEADING2
    if list_items_all_start_with(lines,"### "):
        return BlockType.HEADING3
    if list_items_all_start_with(lines,"#### "):
        return BlockType.HEADING4
    if list_items_all_start_with(lines,"##### "):
        return BlockType.HEADING5
    if list_items_all_start_with(lines,"###### "):
        return BlockType.HEADING6
    if list_items_all_start_with(lines, ">"):
        return BlockType.QUOTE
    if list_items_all_start_with(lines, "- "):
        return BlockType.UNORDERED_LIST
    if list_items_all_start_with(lines, "* "):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    
    