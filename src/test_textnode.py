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

    def test_extract_markdown_images1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_extract_markdown_links1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links2(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        self.assertEqual(split_nodes_link([node]), [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev" )
                ])
        
    def test_split_nodes_link1(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)", TextType.TEXT,)
        self.assertEqual(split_nodes_link([node]), [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
                ])

    def test_split_nodes_link2(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        node2 = TextNode("(Node2) This is text with a link ![IMAGE](https://www.boot.dev/boots.jpg) and [to youtube](https://www.youtube.com/@bootdotdev) with more words", TextType.TEXT,)
        self.assertEqual(split_nodes_link([node, node2]), [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev" ),
                TextNode("(Node2) This is text with a link ![IMAGE](https://www.boot.dev/boots.jpg) and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev" ),
                TextNode(" with more words", TextType.TEXT)
                ])

    def test_split_nodes_image(self):
        node = TextNode("This is text with images ![picture](https://www.boot.dev/boots.jpg) and ![hat](https://www.boot.dev/hat.jpg)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
                TextNode("This is text with images ", TextType.TEXT),
                TextNode("picture", TextType.IMAGE, "https://www.boot.dev/boots.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("hat", TextType.IMAGE, "https://www.boot.dev/hat.jpg" )
                ])
   
    def test_split_nodes_image2(self):
        node = TextNode("This is text with images ![picture](https://www.boot.dev/boots.jpg) and ![hat](https://www.boot.dev/hat.jpg)", TextType.TEXT)
        node2 = TextNode("(Node2) This is text with a link ![IMAGE](https://www.boot.dev/boots.jpg) and [to youtube](https://www.youtube.com/@bootdotdev) with more words", TextType.TEXT,)
        self.assertEqual(split_nodes_image([node, node2]), [
                TextNode("This is text with images ", TextType.TEXT),
                TextNode("picture", TextType.IMAGE, "https://www.boot.dev/boots.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("hat", TextType.IMAGE, "https://www.boot.dev/hat.jpg"),
                TextNode("(Node2) This is text with a link ", TextType.TEXT),
                TextNode("IMAGE", TextType.IMAGE, "https://www.boot.dev/boots.jpg"),
                TextNode(" and [to youtube](https://www.youtube.com/@bootdotdev) with more words", TextType.TEXT)
                ])

#provided tests
    def test_split_image3(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single3(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images4(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links3(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)" 
        self.assertListEqual(text_to_textnodes(text), [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])


    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(text_to_textnodes(text), [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
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