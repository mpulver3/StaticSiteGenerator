from textnode import *

def main(text, text_type, url):
    node = TextNode(text, text_type, url)
    print(node)

main("This is a text node", TextType.BOLD, "https://www.boot.dev")