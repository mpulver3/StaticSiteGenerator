from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):    
        self.text = text 
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
        
    def __repr__(self):
       return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Invalid Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result_nodes.append(old_node)
            continue
        if delimiter != "*" and delimiter != "**" and delimiter != "`":
            raise Exception("Unknown delimiter")
        if old_node.text.startswith(delimiter):
            sub_list = []
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            parts = parts[1:]
            if old_node.text.endswith(delimiter):
                parts = parts[:-1]
            for i in range(0, len(parts)):
                if i % 2 == 0:
                    sub_list.append(TextNode(parts[i], text_type))
                else:
                    sub_list.append(TextNode(parts[i], old_node.text_type))
            result_nodes.extend(sub_list)
        else:
            sub_list = []
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            if old_node.text.endswith(delimiter):
                parts = parts[:-1]
            for i in range(0, len(parts)):
                if i % 2 == 0:
                    sub_list.append(TextNode(parts[i], old_node.text_type))         
                else:
                    sub_list.append(TextNode(parts[i], text_type))
            result_nodes.extend(sub_list)
    return result_nodes
'''
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
'''