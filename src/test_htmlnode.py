import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "this is the text", {"href": "https://www.google.com"})
        node.to_html
    
    def test_props_toHTML(self):
        node = HTMLNode("a", "this is the text", {"href": "https://www.google.com"})
        print(node.props_to_html)

    def test_Neq2(self):
        node = HTMLNode("a", "this is the text", {"href": "https://www.google.com"})
        print(node.__repr__)
    


if __name__ == "__main__":
    unittest.main()
