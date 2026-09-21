from textnode import TextNode, TextType

def split_nodes_delimeter(oldNodes : list[TextNode], delimeter : str, textType : TextType) -> list[TextNode]:
    newNodes : list[TextNode] = []
    for node in oldNodes:
        if node.text_type != TextType.TEXT: #TODO: expand this if
            newNodes.append(node)
            continue

        if list(node.text).count(delimeter) % 2 != 0:
            raise Exception("delimeter is not closed")

        subTexts : list[str] = node.text.split(delimeter)


        currentIsText : bool = not node.text.startswith(delimeter)

        for text in subTexts:
            if text == "":
                continue

            if currentIsText:
                newNodes.append(TextNode(text, TextType.TEXT))

            else:
                newNodes.append(TextNode(text, textType))

            currentIsText = not currentIsText

    return newNodes
