from textnode import TextType, TextNode
from markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.text:
            new_nodes.append(node)
            continue
        split_lines = node.text.split(f"{delimiter}")
        if len(split_lines) % 2 == 0:
            raise Exception("Markdown syntax incorrect or not found")
        for i in range(len(split_lines)):
            if split_lines[i] == "":
                continue
            if i % 2 != 0:
                new_node = TextNode(split_lines[i], text_type, None)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(split_lines[i], TextType.text, None)
                new_nodes.append(new_node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            new_nodes.append(node)
            continue
        current_text = node.text
        extracted_markdown = extract_markdown_images(current_text)
        if len(extracted_markdown) == 0:
            new_nodes.append(node)
            continue
        for markdown in extracted_markdown:
            new_text = current_text.split(f"![{markdown[0]}]({markdown[1]})", 1)
            if len(new_text) != 2:
                raise Exception("Markdown syntax incorrect or not found")
            if new_text[0] != "":
                new_nodes.append(TextNode(new_text[0], TextType.text))
            new_nodes.append(TextNode(markdown[0], TextType.image, markdown[1]))
            current_text = new_text[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            new_nodes.append(node)
            continue
        current_text = node.text
        extracted_markdown = extract_markdown_links(current_text)
        if len(extracted_markdown) == 0:
            new_nodes.append(node)
            continue
        for markdown in extracted_markdown:
            new_text = current_text.split(f"[{markdown[0]}]({markdown[1]})", 1)
            if len(new_text) != 2:
                raise Exception("Markdown syntax incorrect or not found")
            if new_text[0] != "":
                new_nodes.append(TextNode(new_text[0], TextType.text))
            new_nodes.append(TextNode(markdown[0], TextType.link, markdown[1]))
            current_text = new_text[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.text))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = split_nodes_delimiter([TextNode(text, TextType.text)], "**", TextType.bold)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.code)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes