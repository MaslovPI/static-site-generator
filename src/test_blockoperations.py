import unittest
from blockoperations import markdown_to_blocks


class TestBlockOperations(unittest.TestCase):
    def test_should_split_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_should_split_empty_markdown_to_empty_blocks(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [],
            blocks,
        )

    def test_should_split_none_to_empty_blocks(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [],
            blocks,
        )


if __name__ == "__main__":
    unittest.main()
