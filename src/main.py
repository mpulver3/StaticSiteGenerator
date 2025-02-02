from textnode import *
from htmlnode import *

def main(text, text_type, url):
    node = TextNode(text, text_type, url)
    htmlnode = HTMLNode("a", "text", {"href": "https://www.google.com","target": "_blank"})
    print(node)
    print(htmlnode)
    print(htmlnode.props_to_html())

main("This is a text node", TextType.BOLD, "https://www.boot.dev")