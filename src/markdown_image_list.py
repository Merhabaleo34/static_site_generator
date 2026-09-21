from re import findall
from textnode import TextNode, TextType

def extract_images(text: str) -> list[tuple[str,str]]:
    return findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_links(text: str) -> list[tuple[str,str]]:
    return findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


def split_nodes_link(oldNodes: list[TextNode]) -> list[TextNode]:
    newNodes : list[TextNode] = []
    for node in oldNodes:
        if node.url is not None:
            newNodes.append(node)
            continue

        text = node.text
        matches = extract_links(text)
        
        if matches == []:
            newNodes.append(node)
            continue
        
        sub_text = text.split("["+matches[0][0]+"]",1)[0]
        count = 1
        for match in matches:
            if sub_text != "":
                node1 = TextNode(sub_text, node.text_type)
                newNodes.append(node1)

            link_node = TextNode(match[0], TextType.LINK, match[1])
            newNodes.append(link_node)
            if count == len(matches):
                sub_text_list = text.split("("+match[1]+")",1)[1].split("["+match[0]+"]",1)
                for text1 in sub_text_list:
                    if text1 != "" or text1 != "\n":
                        node1 = TextNode(text1, node.text_type)
                        newNodes.append(node1)
                continue

            sub_text = text.split("("+match[1]+")",1)[1].split("["+matches[count][0]+"]",1)[0]
            count += 1
            

    return newNodes

def split_nodes_image(oldNodes: list[TextNode]) -> list[TextNode]:
    newNodes : list[TextNode] = []
    for node in oldNodes:
        if node.url is not None:
            newNodes.append(node)
            continue

        text = node.text
        matches = extract_images(text)
        
        if matches == []:
            newNodes.append(node)
            continue
        
        sub_text = text.split("!["+matches[0][0]+"]",1)[0]
        count = 1
        for match in matches:
            if sub_text != "":
                node1 = TextNode(sub_text, node.text_type)
                newNodes.append(node1)
    
            image_node = TextNode(match[0], TextType.IMAGE, match[1])
            newNodes.append(image_node)
            if count == len(matches):
                sub_text_list = text.split("("+match[1]+")",1)[1].split("!["+match[0]+"]",1)
                for text1 in sub_text_list:
                    if text1 != "":
                        node1 = TextNode(text1, node.text_type)
                        newNodes.append(node1)
                continue

            sub_text = text.split("("+match[1]+")",1)[1].split("!["+matches[count][0]+"]",1)[0]
            count += 1



    return newNodes




