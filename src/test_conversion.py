import unittest

from textnode import TextNode, TextType
from conversion import text_node_to_html_node


class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(None, html_node.tag)
        self.assertEqual("This is a text node", html_node.value)

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual("b", html_node.tag)
        self.assertEqual("This is a bold node", html_node.value)

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual("i", html_node.tag)
        self.assertEqual("This is a italic node", html_node.value)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual("code", html_node.tag)
        self.assertEqual("This is a code node", html_node.value)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "http://link.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual("a", html_node.tag)
        self.assertEqual("This is a link node", html_node.value)
        self.assertIsNotNone(html_node.props)
        self.assertEqual("http://link.url", html_node.props["href"])

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "http://link.url")
        html_node = text_node_to_html_node(node)
        self.assertEqual("img", html_node.tag)
        self.assertEqual("", html_node.value)
        self.assertIsNotNone(html_node.props)
        self.assertEqual("http://link.url", html_node.props["src"])
        self.assertEqual("This is an image node", html_node.props["alt"])


if __name__ == "__main__":
    unittest.main()
