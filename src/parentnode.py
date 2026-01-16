from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is not provided")

        if not self.children:
            raise ValueError("Children are not provided")

        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{''.join(child.to_html() for child in self.children)}"
            f"</{self.tag}>"
        )
