def markdown_to_blocks(markdown):
    return [stripped for p in markdown.split("\n\n") if (stripped := p.strip())]
