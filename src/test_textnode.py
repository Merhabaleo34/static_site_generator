import unittest
from textnode import TextNode, TextType

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
        self.assertEqual(str(node),"TextNode(This is a text node, bold, None)" )

if __name__ == "__main__":
    unittest.main()
