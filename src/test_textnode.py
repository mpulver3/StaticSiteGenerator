import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_Neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_Neq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_Neq3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node, node2)   

    def test_text_to_html(self):
        tnode = TextNode("This is a text node", TextType.BOLD)
        hnode = text_node_to_html_node(tnode)
        check_leaf = LeafNode("b", "This is a text node")
        self.assertEqual(str(hnode), str(check_leaf))

    def test_text_to_html2(self):
        tnode = TextNode("This is a node", TextType.ITALIC)
        hnode = text_node_to_html_node(tnode)
        check_leaf = LeafNode("i", "This is a node")
        self.assertEqual(str(hnode), str(check_leaf))

    def test_text_to_html3(self):
        tnode = TextNode("This is a text node", TextType.LINK, "www.google.com")
        hnode = text_node_to_html_node(tnode)
        check_leaf = LeafNode("a", "This is a text node", {"href": "www.google.com"})
        self.assertEqual(str(hnode), str(check_leaf))

    def test_text_to_html4(self):
        tnode = TextNode("Description", TextType.IMAGE, url="www.example.com/img.jpg")
        hnode = text_node_to_html_node(tnode)
        check_leaf = LeafNode("img", "", {"src": "www.example.com/img.jpg", "alt": "Description"})
        self.assertEqual(str(hnode), str(check_leaf))

    def test_split_nodes_delimiter(self):
        tnode = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([tnode], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter2(self):
        tnode = TextNode("**This** is text with a **BOLD** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([tnode], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with a ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter3(self):
        tnode = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([tnode], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

if __name__ == "__main__":
    unittest.main()


'''
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
'''