import unittest

from textnode import TextNode, TextType
from nodeoperations import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)


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

    def test_should_extract_one_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_should_extract_multiple_images(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
            + " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        matches = extract_markdown_images(text)
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_should_extract_one_link(self):
        matches = extract_markdown_links(
            "This is text with an [to an image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("to an image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_should_extract_multiple_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            + "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(text)
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_should_not_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an [to an image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_should_not_extract_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_should_split_images(self):
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_should_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_should_split_single_image(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_should_split_single_link(self):
        node = TextNode(
            "[link text](https://www.example.COM/page)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "https://www.example.COM/page"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
