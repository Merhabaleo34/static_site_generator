import textnode

def main():
    text_type = textnode.TextType.BOLD
    text_node = textnode.TextNode("test text",text_type,"https://localhost:8888")
    print(text_node)


if __name__ == "__main__":
    main()
