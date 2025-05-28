import unittest

from textnode import TextNode, TextType
from inline_markdown import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("dummy data", TextType.TEXT, "https://www.abecode.com")
        node2 = TextNode("dummy data", TextType.TEXT, "https://www.abecodes.com")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("dummy data", TextType.TEXT, "https://www.abecode.com")
        node2 = TextNode("Frontend gives me a headache", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_eq4(self):
        node = TextNode("You can't handle the truth!", TextType.TEXT, "https://www.abecodes.com")
        node2 = TextNode("My name is slim shady", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text(self):
        node = TextNode("This is alt text", TextType.IMAGE, "http://www.unsplash.com/imagexxxxxx")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"src":"http://www.unsplash.com/imagexxxxxx", "alt":"This is alt text"})

if __name__ == "__main__":
    unittest.main()