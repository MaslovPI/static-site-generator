import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.TEXT:
            new_nodes.append(node)
            continue
        sub_nodes = node.text.split(delimiter)

        if len(sub_nodes) % 2 == 0:
            raise ValueError("Formatting block is not closed in TextNode")

        new_nodes.extend(prepare_sub_nodes(sub_nodes, text_type))
    return new_nodes


def prepare_sub_nodes(sub_nodes, text_type):
    new_nodes = []
    for index, sub_node in enumerate(sub_nodes):
        if not sub_node:
            continue

        new_nodes.append(
            TextNode(sub_node, TextType.TEXT if index % 2 == 0 else text_type)
        )
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
