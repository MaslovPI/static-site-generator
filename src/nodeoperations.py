import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type: TextType):
    return [
        item
        for node in old_nodes
        for item in split_node_delimiter(node, delimiter, text_type)
    ]


def split_node_delimiter(node: TextNode, delimiter, text_type: TextType):
    if not node.text_type == TextType.TEXT:
        return [node]

    sub_nodes = node.text.split(delimiter)

    if len(sub_nodes) % 2 == 0:
        raise ValueError("Formatting block is not closed in TextNode")

    return prepare_sub_nodes(sub_nodes, text_type)


def prepare_sub_nodes(sub_nodes, text_type):
    new_nodes = []
    for index, sub_node in enumerate(sub_nodes):
        if not sub_node:
            continue

        new_nodes.append(
            TextNode(sub_node, TextType.TEXT if index % 2 == 0 else text_type)
        )
    return new_nodes


def split_nodes_link(old_nodes):
    return [item for node in old_nodes for item in split_node_link(node)]


def split_node_link(node: TextNode):
    if not node.text_type == TextType.TEXT:
        return [node]
    matches = extract_markdown_links(node.text)
    if not matches:
        return [node]
    return process_link_matches_to_nodes(node.text, matches)


def process_link_matches_to_nodes(text, matches):
    new_nodes = []
    text_to_process = text
    for link_text, link_url in matches:
        sections = text_to_process.split(f"[{link_text}]({link_url})", 1)
        if len(sections) != 2:
            raise ValueError("Something went wrong processing markdown link")
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
        text_to_process = sections[1]
    if text_to_process:
        new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    return [item for node in old_nodes for item in split_node_image(node)]


def split_node_image(node: TextNode):
    if not node.text_type == TextType.TEXT:
        return [node]
    matches = extract_markdown_images(node.text)
    if not matches:
        return [node]
    return process_image_matches_to_nodes(node.text, matches)


def process_image_matches_to_nodes(text, matches):
    new_nodes = []
    text_to_process = text
    for alt_text, image_url in matches:
        sections = text_to_process.split(f"![{alt_text}]({image_url})", 1)
        if len(sections) != 2:
            raise ValueError("Something went wrong processing markdown image")
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
        text_to_process = sections[1]
    if text_to_process:
        new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
