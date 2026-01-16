import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_no_props_should_result_in_empty_string(self):
        node = HTMLNode(props={})
        self.assertEqual("", node.props_to_html())

    def test_none_props_should_result_in_empty_string(self):
        node = HTMLNode(props=None)
        self.assertEqual("", node.props_to_html())

    def test_should_convert_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )


if __name__ == "__main__":
    unittest.main()
