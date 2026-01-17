from blocktype import BlockType


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
