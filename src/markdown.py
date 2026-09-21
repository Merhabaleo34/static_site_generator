from enum import Enum

def markdown_to_block(markdown:str) -> list[str]:
    lines = markdown.split("\n\n")
    actual_lines = []
    for line in lines:
        new_line = line.strip(" \n")

        if new_line == "":
            continue

        actual_lines.append(new_line)

    return actual_lines


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(markdown: str):
    is_heading = True
    i = 0
    if markdown[0] != "#":
        is_heading = False
    while i<6:
        if markdown[i] != "#":
            break
        i += 1
    else:
        i -= 1
    if markdown[i]!=" ":
        is_heading = False

    if is_heading:
        return BlockType.HEADING

    if markdown.startswith("```\n") and markdown.endswith("\n```"):
        return BlockType.CODE

    lines = markdown.split("\n")
    starts_with_quote = True

    for line in lines:
        if not line.startswith(">"):
            starts_with_quote = False
            break
    if starts_with_quote:
        return BlockType.QUOTE

    starts_with_unlist = True

    for line in lines:
        if not line.startswith("- "):
            starts_with_unlist = False
            break
    if starts_with_unlist:
        return BlockType.UNORDERED_LIST

    starts_with_list = True

    count = 1
    for line in lines:
        if not line[0].isdigit():
            starts_with_list = False
            break
        
        if line[1:3] != ". ":
            starts_with_list = False
            break
        
        if line[0] != str(count):
            starts_with_list = False
            break

        count += 1
    if starts_with_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH




