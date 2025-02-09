from enum import Enum
from htmlnode import *
import re

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
    
#converts a text node to html node
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

#takes raw markdown formatted text and returns a list of tuples. Each tuple = is the alt text & image URL
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

#takes raw markdown formatted text and returns a list of tuples. Each tuple = is the link text & link URL
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

#splits text node(s) into new nodes based on the given delimiter
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


def split_nodes_image(old_nodes):
    list_of_new_nodes = []
    for old_node in old_nodes:
        def inner(input_string):
            split_string_list = re.findall(r"!\[.*?\]\(.*?\)", input_string)
            if split_string_list == []:
                return [TextNode(input_string, TextType.TEXT)]
            sub_list = []
            split_string = split_string_list[0]
            parts = input_string.split(split_string)
            #covers the case where the link is non unique. Rejoins all but the first division
            if len(parts) > 2:
                temp_list = [parts[0]]
                temp_string = ""
                for i in range(1, len(parts)):
                    if i < len(parts) - 1:
                        temp_string += (parts[i] + split_string)
                    else:
                        temp_string += parts[i]
                temp_list.append(temp_string)
                parts = temp_list
            if parts[0] != "":
                sub_list.append(TextNode(parts[0], TextType.TEXT))
            text_link_list = re.findall(r"\[(.*?)\]", split_string) 
            url_link_list = (re.findall(r"\((.*?)\)", split_string))
            sub_list.append(TextNode(text_link_list[0], TextType.IMAGE, url=url_link_list[0]))
            if parts[1] != "":
                sub_list.extend(inner(parts[1]))
            return sub_list
        list_of_new_nodes.extend(inner(old_node.text))
    return list_of_new_nodes


     
def split_nodes_link(old_nodes):
    list_of_new_nodes = []
    for old_node in old_nodes:
        def inner(input_string):
            split_string_list = re.findall(r"(?<!!)\[.*?\]\(.*?\)", input_string)
            if split_string_list == []:
                return [TextNode(input_string, TextType.TEXT)]
            sub_list = []
            split_string = split_string_list[0]
            parts = input_string.split(split_string)
            #covers the case where the link is non unique. Rejoins all but the first division
            if len(parts) > 2:
                temp_list = [parts[0]]
                temp_string = ""
                for i in range(1, len(parts)):
                    if i < len(parts) - 1:
                        temp_string += (parts[i] + split_string)
                    else:
                        temp_string += parts[i]
                temp_list.append(temp_string)
                parts = temp_list
            if parts[0] != "":
                sub_list.append(TextNode(parts[0], TextType.TEXT))
            text_link_list = re.findall(r"\[(.*?)\]", split_string) 
            url_link_list = (re.findall(r"\((.*?)\)", split_string))
            sub_list.append(TextNode(text_link_list[0], TextType.LINK, url=url_link_list[0]))
            if parts[1] != "":
                sub_list.extend(inner(parts[1]))
            return sub_list
        list_of_new_nodes.extend(inner(old_node.text))
    return list_of_new_nodes








'''

text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

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