import unittest
from blockoperations import block_to_block_type, markdown_to_blocks
from blocktype import BlockType


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

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "## heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "#### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "##### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "1. list\n5. items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
