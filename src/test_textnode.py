import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_should_be_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_should_not_be_eq_when_type_different(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_should_not_be_eq_when_text_different(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("Different text", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_should_not_be_eq_when_url_different(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        node2 = TextNode("This is a text node", TextType.LINK, "http://some.url")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
