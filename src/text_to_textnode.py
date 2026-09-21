from textnode import TextNode, TextType
from markdown_image_list import split_nodes_link, split_nodes_image
from delimiter import split_nodes_delimeter

def text_to_text_node(text:str):
    node = [TextNode(text, TextType.TEXT)]
    node_bold = split_nodes_delimeter(node, "**", TextType.BOLD)
    node_italic = split_nodes_delimeter(node_bold, "_", TextType.ITALIC)
    node_code = split_nodes_delimeter(node_italic, "`", TextType.CODE)
    node_image = split_nodes_image(node_code)
    node_link = split_nodes_link(node_image)
    return node_link


