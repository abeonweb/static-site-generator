import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode




class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        props={
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "link tag", [], props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_eq2(self):
        props={
            "class":"test",
        }
        node = HTMLNode("p", "paragraph tag", [], props)
        self.assertNotEqual(node, '')

    def test_eq3(self):
        props={
            "class":"test",
        }
        node = HTMLNode("div", "generic div tag", [], props)
        self.assertNotEqual(node, '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        props={
            "class":"test",
        }
        node = LeafNode("div", "generic div tag", props)
        self.assertEqual(node.to_html(), '<div class="test">generic div tag</div>')
    
    def test_leaf_to_html_a(self):
        props={
            "href":"https://www.google.com",
            "class":"link_styles",
        }
        node = LeafNode("a", "Go Home", props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" class="link_styles">Go Home</a>')

    def test_leaf_to_html_no_props(self): 
        node = LeafNode("a", "Go Home", [])
        self.assertNotEqual(node.to_html(), '<a href="https://www.google.com" class="link_styles">Go Home</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
            grandchild_node = LeafNode("b", "grandchild")
            child_node = ParentNode("span", [grandchild_node])
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b></span></div>",
            )