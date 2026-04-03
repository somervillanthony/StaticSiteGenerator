from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    text = "text"
    italic = "italic"
    bold = "bold"
    code = "code"
    link = "link"
    image = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"    

def text_node_to_html_node(text_node):
        if text_node.text_type not in TextType:
            raise Exception("Invalid text type")
        match (text_node.text_type):
            case TextType.text:
                return LeafNode(None, text_node.text)
            case TextType.bold:
                return LeafNode("b", text_node.text)
            case TextType.italic:
                return LeafNode("i", text_node.text)
            case TextType.code:
                return LeafNode("code", text_node.text)
            case TextType.link:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.image:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})