import unittest

from textnode import TextNode, TextType
from nodeoperations import split_nodes_delimiter


class TestNodeOperations(unittest.TestCase):
    def test_should_split_one_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(TextNode("This is text with a ", TextType.TEXT), new_nodes[0])
        self.assertEqual(TextNode("code block", TextType.CODE), new_nodes[1])
        self.assertEqual(TextNode(" word", TextType.TEXT), new_nodes[2])

    def test_should_split_one_bold_block(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(TextNode("This is text with a ", TextType.TEXT), new_nodes[0])
        self.assertEqual(TextNode("bold block", TextType.BOLD), new_nodes[1])
        self.assertEqual(TextNode(" word", TextType.TEXT), new_nodes[2])

    def test_should_split_one_italic_block(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(TextNode("This is text with a ", TextType.TEXT), new_nodes[0])
        self.assertEqual(TextNode("italic block", TextType.ITALIC), new_nodes[1])
        self.assertEqual(TextNode(" word", TextType.TEXT), new_nodes[2])

    def test_should_split_multiple_bold_block(self):
        node = TextNode(
            "This is text with several **bold blocks** like **this**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(4, len(new_nodes))
        self.assertEqual(
            TextNode("This is text with several ", TextType.TEXT), new_nodes[0]
        )
        self.assertEqual(TextNode("bold blocks", TextType.BOLD), new_nodes[1])
        self.assertEqual(TextNode(" like ", TextType.TEXT), new_nodes[2])
        self.assertEqual(TextNode("this", TextType.BOLD), new_nodes[3])

    def test_should_raise_exception_with_unclosed_block(self):
        node = TextNode("This is text with **unclosed bold block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
