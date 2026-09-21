import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from delimiter import split_nodes_delimeter
from markdown_image_list import extract_images, extract_links, split_nodes_image, split_nodes_link
from text_to_textnode import text_to_text_node
from markdown import markdown_to_block, block_to_block_type, BlockType
from markdown_to_node import markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://localhost:8888")
        self.assertEqual(str(node),"TextNode(This is a text node, bold, https://localhost:8888)")

    def test_repr_noUrl(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node),"TextNode(This is a text node, bold, None)")

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        children = HTMLNode("h1","muhaha", None, {"href": "https://www.google.com","target": "_blank"})
        node = HTMLNode("p","no text for you",[children],{"target": "_blank"})
        self.assertEqual(str(node),"HTMLNode(TAG = p, VALUE = no text for you, CHILDREN = [HTMLNode(TAG = h1, VALUE = muhaha, CHILDREN = None, PROPS =  href=\"https://www.google.com\" target=\"_blank\")], PROPS =  target=\"_blank\")")
        

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_repr(self):
        node = LeafNode("p", "Hello world", {"href":"https://www.google.com"})
        self.assertEqual(node.__repr__(),"LeafNode(TAG = p, VALUE = Hello world, PROPS =  href=\"https://www.google.com\")")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Hello world", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Hello world</a>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(indentation=2), "<div>\n  <span>child</span>\n</div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(indentation=2),
            "<div>\n  <span>\n    <b>grandchild</b>\n  </span>\n</div>",
        )

    def test_to_html_with_multiple_children(self):
        first_child = LeafNode("b","first child")
        second_child = LeafNode("i","second child")
        parent_node = ParentNode("div",[first_child,second_child])
        self.assertEqual(
            parent_node.to_html(indentation=2),
            "<div>\n  <b>first child</b>\n  <i>second child</i>\n</div>",
        )

    def test_to_html_with_a_family(self):
        first_child = LeafNode("b","first child")
        second_child = LeafNode("i","second child")
        grandparent = ParentNode("span",[first_child])
        node = ParentNode("div",[second_child,grandparent])
        self.assertEqual(
            node.to_html(indentation=2),
            "<div>\n  <i>second child</i>\n  <span>\n    <b>first child</b>\n  </span>\n</div>",
        )


class TestTextNode_to_HTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://bootdotdev.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src":"https://bootdotdev.com","alt":"This is an image node"})

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"https://google.com"})

class TestSplitDelimiter(unittest.TestCase):

    def test_bold_middle(self):
        node = TextNode("This is text with a **bold cool** word", TextType.TEXT)
        newNodes = split_nodes_delimeter([node],"**",TextType.BOLD)
        self.assertEqual(newNodes,
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("bold cool", TextType.BOLD),
                          TextNode(" word", TextType.TEXT)])

    def test_begins_with(self):
        node = TextNode("_This is text_ with an italic cool word", TextType.TEXT)
        newNodes = split_nodes_delimeter([node],"_",TextType.ITALIC)
        self.assertEqual(newNodes,
                         [TextNode("This is text", TextType.ITALIC),
                          TextNode(" with an italic cool word", TextType.TEXT)])

    def test_end_with(self):
        node = TextNode("This is text with a **bold cool word**", TextType.TEXT)
        newNodes = split_nodes_delimeter([node],"**",TextType.BOLD)
        self.assertEqual(newNodes,
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("bold cool word", TextType.BOLD)])

    def test_multiple_delimiter(self):
        node = TextNode("**This is text** with a **bold cool** word", TextType.TEXT)
        newNodes = split_nodes_delimeter([node],"**",TextType.BOLD)
        self.assertEqual(newNodes,
                         [TextNode("This is text", TextType.BOLD),
                          TextNode(" with a ", TextType.TEXT),
                          TextNode("bold cool", TextType.BOLD),
                          TextNode(" word", TextType.TEXT)])

    def test_multiple_nodes(self):
        node1 = TextNode("This is text with a **bold cool** word", TextType.TEXT)
        node2 = TextNode("I **HATE** writing unit tests", TextType.TEXT)
        newNodes = split_nodes_delimeter([node1,node2],"**",TextType.BOLD)
        self.assertEqual(newNodes,
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("bold cool", TextType.BOLD),
                          TextNode(" word", TextType.TEXT),
                          TextNode("I ",TextType.TEXT),
                          TextNode("HATE", TextType.BOLD),
                          TextNode(" writing unit tests", TextType.TEXT)])

    def test_delimeter_is_not_closed(self):
        node = TextNode("This is** text** with a **bold cool word", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimeter, node, TextType.BOLD)

class TestLink_Image(unittest.TestCase):

    def test_extract_markdown_images(self):

       matches = extract_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
       )

       self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertEqual(matches,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_link(self):

        matches = extract_links("This is text with a link [to boot dev](https://www.boot.dev)")
        
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_multiple_links(self):

        text = extract_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        
        self.assertEqual(text,
         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

class TestLink_ImageSplit(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_first_is_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_images(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is not a text with ![not an image](https://i.imgssur.com/zjjsdşbsoscjıhjcJKZ.png) and not another ![second'nt image](httpsxx://i.imgurldlcl.com/3elNhdsgdfQu.png)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is not a text with ", TextType.BOLD),
                TextNode("not an image", TextType.IMAGE, "https://i.imgssur.com/zjjsdşbsoscjıhjcJKZ.png"),
                TextNode(" and not another ", TextType.BOLD),
                TextNode("second'nt image", TextType.IMAGE, "httpsxx://i.imgurldlcl.com/3elNhdsgdfQu.png"),
            ],
            new_nodes,
        )
    def test_no_images(self):
        node = TextNode("This is a node with no image or link",TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes, [TextNode("This is a node with no image or link",TextType.TEXT)])


    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_begins_with_links(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


    def test_split_multiple_links(self):
        node1 = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is not a text with [not a link](https://i.imgssur.com/zjjsdşbsoscjıhjcJKZ.png) and not another [second'nt link](httpsxx://i.imgurldlcl.com/3elNhdsgdfQu.png)",
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is not a text with ", TextType.BOLD),
                TextNode("not a link", TextType.LINK, "https://i.imgssur.com/zjjsdşbsoscjıhjcJKZ.png"),
                TextNode(" and not another ", TextType.BOLD),
                TextNode("second'nt link", TextType.LINK, "httpsxx://i.imgurldlcl.com/3elNhdsgdfQu.png"),
            ],
            new_nodes,
        )

    def test_no_link(self):
        node = TextNode("This is a node with no image or link",TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes, [TextNode("This is a node with no image or link",TextType.TEXT)])

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_node(text)

        self.assertEqual(nodes,[
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_block(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_heading(self):
        markdown_var = "# This is a heading"
        
        markdown1 = "## This is also a heading"

        markdown2 = "#### This is another heading"

        markdown3 = "####### This is not a heading"

        block_type = block_to_block_type(markdown_var)
        block_type1 = block_to_block_type(markdown1)
        block_type2 = block_to_block_type(markdown2)
        block_type3 = block_to_block_type(markdown3)

        self.assertEqual(block_type, BlockType.HEADING)
        self.assertEqual(block_type1, BlockType.HEADING)
        self.assertEqual(block_type2, BlockType.HEADING)
        self.assertEqual(block_type3, BlockType.PARAGRAPH)

    def test_block_to_blocktype_code(self):
        markdown_var = "```\nThis is a \ncode block\n```"
        block_type = block_to_block_type(markdown_var)
        
        markdown1 = "``\n This is not```\n"
        block_type1 = block_to_block_type(markdown1)

        self.assertEqual(block_type,BlockType.CODE)
        self.assertEqual(block_type1,BlockType.PARAGRAPH)

    def test_paragraph(self):
        markdown_var ="This is a simple paragraph."
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        markdown_var ="""This is a paragraph
that spans multiple lines
but is still one block."""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_line_in_middle_paragraph(self):
        markdown_var ="This is a - simple paragraph."
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list(self):
        markdown_var ="""- First item
- Second item
- Third item"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_single_item_list(self):
        markdown_var = "- Only item"
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list(self):
        markdown_var ="""- First item
This isn't a list item
- Third item"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_no_space(self):
        markdown_var ="""-First item
-Second item"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        markdown_var ="""1. First item
2. Second item
3. Third item"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_one_item(self):
        markdown_var ="1. First item"
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_numbering_error(self):
        markdown_var ="""1. First
2. Second
4. Fourth"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_numbering_error2(self):
        markdown_var ="""2. Second
3. Third
4. Fourth"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_empty_space(self):
        markdown_var ="""2. Second
3.Third
4. Fourth"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote(self):
        markdown_var =">This is a simple quote."
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_multiline(self):
        markdown_var ="""> First line
> Second line
> Third line"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.QUOTE)

    
    def test_invalid_quote(self):
        markdown_var ="""> First line
Second line
> Third line"""
        block_type = block_to_block_type(markdown_var)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,"""<div>
    <p>
        This is 
        <b>bolded</b>
         paragraph text in a p tag here
    </p>
    <p>
        This is another paragraph with 
        <i>italic</i>
         text and 
        <code>code</code>
         here
    </p>
</div>""",
        )
    
    
    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        """<div>
    <pre>
        <code>
        This is text that _should_ remain
        the **same** even with inline stuff
        </code>
    </pre>
</div>""",
    )









if __name__ == "__main__":
    unittest.main()
