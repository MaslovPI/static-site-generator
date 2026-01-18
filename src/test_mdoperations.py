import unittest

from blocktype import BlockType
from mdoperations import (
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title,
)


class TestMDOperations(unittest.TestCase):
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
        block = "> quote\n>\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "1. list\n5. items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            + "<p>This is another paragraph with <i>italic</i> "
            + "text and <code>code</code> here</p></div>",
            html,
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ul><li>This is a list</li><li>with items</li>"
            + "<li>and <i>more</i> items</li></ul><ol>"
            + "<li>This is an <code>ordered</code> list</li>"
            + "<li>with items</li><li>and more items</li></ol></div>",
            html,
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
            html,
        )

    def test_blockquote(self):
        md = """
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            '<div><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote><p>this is paragraph text</p></div>',
            html,
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
            html,
        )

    def test_should_extract_title(self):
        md = """
this is not a title

## this is also not a title

# this is a title

# this is somewhat a title, but really not
        """
        title = extract_title(md)
        self.assertEqual("this is a title", title)

    def test_should_fail_when_cant_extract_title(self):
        md = """
this doc does not have a title
        """
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
