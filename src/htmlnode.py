class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("To be defined in child classes")

    def props_to_html(self):
        result = ""

        if not self.props:
            return result

        for prop in self.props.items():
            result += f' {prop[0]}="{prop[1]}"'
        return result

    def __repr__(self) -> str:
        has_children = (
            f"Has {len(self.children)} children" if self.children else "Has no children"
        )

        return (
            "HTMLNode("
            f"tag = {self.tag}, value = {self.value}, "
            f"{has_children}, props = '{self.props_to_html()}')"
        )
