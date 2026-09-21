from markdown import BlockType, block_to_block_type, markdown_to_block
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from text_to_textnode import text_to_text_node
import re


def markdown_to_html_node(markdown_var: str) -> HTMLNode:
    blocks = markdown_to_block(markdown_var)
    html_cildren = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block,block_type)
        html_cildren.append(node)
    return ParentNode(tag= "div", children= html_cildren)



def block_to_html_node(block:str,block_type: BlockType) -> HTMLNode:
    if block_type==BlockType.PARAGRAPH:
        return ParentNode(tag="p",children= text_to_children(block.replace("\n", " ")))

    elif block_type==BlockType.HEADING:
        number = 0
        for i in block:
            if i != "#":
                break
            number += 1
        return ParentNode(tag="h"+str(number),children= text_to_children(block.strip("# ")))

    elif block_type==BlockType.CODE:
        node = TextNode(text=block.strip("`"), text_type=TextType.CODE)
        html= text_node_to_html_node(node)
        return ParentNode(tag="pre",children=[html])


    elif block_type==BlockType.QUOTE:
        return ParentNode(tag="blockquote",children= text_to_children(block.strip("> ").replace("\n"," ")))

    elif block_type==BlockType.UNORDERED_LIST:
        members = block.split("- ")
        children_list = []
        for member in members[1::]:
            children_list.append(ParentNode(tag="li", children=text_to_children(member)))
        return ParentNode(tag= "ul", children=children_list)

    elif block_type==BlockType.ORDERED_LIST:
        members = block.split(". ")
        children_list = []
        for member in members[1::]:
            children_list.append(ParentNode(tag="li",children=text_to_children(member[:len(member)-2].strip("- "))))
        return ParentNode(tag= "ul", children=children_list)



def text_to_children(text: str):
    nodes = text_to_text_node(text)
    children = []

    for node in nodes:
        children.append(text_node_to_html_node(node))

    return children
