import re
from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import text_to_textnodes

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    extra_line_count = 0
    strings = markdown.split("\n\n")
    for i in range(len(strings)):
        strings[i] = strings[i].strip()
        if strings[i] == "":
            extra_line_count += 1
    for i in range(extra_line_count):
        strings.remove("")
    return strings

def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.heading
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.code
    test_lines = markdown.split("\n")
    valid_quote = True
    valid_ordered_list = True
    valid_unordered_list = True
    line_count = 0
    for line in test_lines:
        if line == "" or line == "\n":
            continue
        line_count += 1
        if line[0] != ">":
            valid_quote = False
        if line[0:2] != "- ":
            valid_unordered_list = False
        split_line = line.split(".")
        if not re.match(r"\d\. ", line) or int(split_line[0]) != line_count:
            valid_ordered_list = False
    if valid_quote == True:
        return BlockType.quote
    if valid_ordered_list == True:
        return BlockType.ordered_list
    if valid_unordered_list == True:
        return BlockType.unordered_list
    return BlockType.paragraph
    
def markdown_to_html_node(markdown):
    parents = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.paragraph:
                block_node = paragraph_node(block)
            case BlockType.heading:
                block_node = heading_node(block)
            case BlockType.code:
                block_node = code_node(block)
            case BlockType.ordered_list:
                block_node = ordered_list_node(block)
            case BlockType.unordered_list:
                block_node = unordered_list_node(block)
            case BlockType.quote:
                block_node = quote_node(block)
        parents.append(block_node)
    return ParentNode("div", parents)

        
def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for node in textnodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes

def paragraph_node(text):
    new_text = text.replace("\n", " ")
    children = text_to_children(new_text)
    return ParentNode("p", children)

def heading_node(text):
    split_text = text.split(" ", 1)
    head_num = len(split_text[0])
    children = text_to_children(split_text[1])
    return ParentNode(f"h{head_num}", children)

def code_node(text):
    new_text = text.replace("```", "").lstrip("\n")
    children = [text_node_to_html_node(TextNode(new_text, TextType.code))]
    return ParentNode("pre", children)

def ordered_list_node(text):
    children = []
    lines = text.split("\n")
    for line in lines:
        split_line = line.split(". ", 1)
        children.append(ParentNode("li", text_to_children(split_line[1])))
    return ParentNode("ol", children)

def unordered_list_node(text):
    children = []
    lines = text.split("\n")
    for line in lines:
        split_line = line.split("- ", 1)
        children.append(ParentNode("li", text_to_children(split_line[1])))
    return ParentNode("ul", children)

def quote_node(text):
    new_text = ""
    lines = text.split("\n")
    stripped_lines = []
    for line in lines:
        split_line = line.split("> ")
        if len(split_line) > 1:
            stripped_lines.append(split_line[1])
        else:
            stripped_lines.append("\n")
    new_text = "\n".join(stripped_lines)  
    return ParentNode("blockquote", text_to_children(new_text))