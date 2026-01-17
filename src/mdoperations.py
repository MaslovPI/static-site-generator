from textnode import TextNode, TextType
from blocktype import BlockType
from parentnode import ParentNode
from conversion import text_node_to_html_node
from nodeoperations import text_to_textnodes


def markdown_to_html_node(markdown) -> ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        children.append(block_to_html_block(block))
    return ParentNode("div", children)


def block_to_html_block(block):
    block_type = block_to_block_type(block)
    lines = block.split("\n")
    match block_type:
        case BlockType.HEADING:
            text = block.split("# ")[1].strip()
            children = text_to_children(text)
            return ParentNode(get_heading_html_tag(block), children)
        case BlockType.QUOTE:
            return lines_to_quote(lines)
        case BlockType.CODE:
            text_node = TextNode(block.strip("`").strip(), TextType.CODE)
            child = text_node_to_html_node(text_node)
            return ParentNode("pre", [child])
        case BlockType.OLIST:
            return ParentNode("ol", lines_to_list_items(lines, ". "))
        case BlockType.ULIST:
            return ParentNode("ul", lines_to_list_items(lines, "- "))
        case BlockType.PARAGRAPH:
            return ParentNode(
                "p", text_to_children(str(block).replace("\n", " ").strip())
            )


def lines_to_list_items(lines, delimiter):
    return [
        ParentNode("li", text_to_children(line.split(delimiter)[1])) for line in lines
    ]


def lines_to_quote(lines):
    return ParentNode(
        "blockquote",
        text_to_children(" ".join(map(lambda line: line.split("> ")[1], lines))),
    )


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def get_heading_html_tag(block):
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"
    raise ValueError("Unexpected prefix on heading")


def markdown_to_blocks(markdown):
    return [stripped for p in markdown.split("\n\n") if (stripped := p.strip())]


def block_to_block_type(block) -> BlockType:
    if is_heading(block):
        return BlockType.HEADING

    lines = block.split("\n")
    if is_code(lines):
        return BlockType.CODE
    if is_quote(lines):
        return BlockType.QUOTE
    if is_ulist(lines):
        return BlockType.ULIST
    if is_olist(lines):
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def is_heading(block):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))


def is_code(lines):
    return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")


def is_quote(lines):
    return all(line.startswith("> ") for line in lines)


def is_ulist(lines):
    return all(line.startswith("- ") for line in lines)


def is_olist(lines):
    return all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines))
