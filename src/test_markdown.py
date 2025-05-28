import unittest
from textnode import TextNode, TextType
from inline_markdown import *

class MarkdownTest(unittest.TestCase):
    # def test_delimiter_end(self):
    #     node = TextNode("This ends with a `code block`", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    #     self.assertEqual([TextNode("This ends with a ", TextType.TEXT), TextNode("code block", TextType.CODE)], new_nodes)

    # def test_delimiter_bold(self):
    #     node = TextNode("This has **bold** text", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    #     self.assertEqual([TextNode("This has ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.TEXT)], new_nodes)
    
    # def test_delimiter_double_italic(self):
    #     node = TextNode("_This has italic_ text _twice_", TextType.TEXT)
    #     new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    #     self.assertEqual([TextNode("This has italic", TextType.ITALIC), TextNode(" text ", TextType.TEXT), TextNode("twice", TextType.ITALIC)], new_nodes)

    # # images
    # def test_extract_markdown_images(self):
    #     matches = extract_markdown_images(
    #         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    #     )
    #     self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    # def test_extract_markdown_images_no_matches(self):
    #     matches = extract_markdown_images(
    #         "This is text with no images"
    #     )
    #     self.assertListEqual([], matches)

    # links
    def test_extract_markdown_link(self):
        matches = extract_markdown_links("- [Abe's website](http://www.abecodes.com). You can also use [Google](http://google.com)")
        self.assertListEqual([("Abe's website","http://www.abecodes.com"), ("Google","http://google.com")], matches)

    def test_extract_markdown_link_no_matches(self):
        matches = extract_markdown_links("There is no match")
        self.assertListEqual([],matches)

    # markdown to text node
    def test_split_images(self):
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
    
    def test_split_links(self):
        node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
    )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )
    def test_split_links_from_list(self):
        node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
    )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) is last")
        self.assertListEqual(
            [
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
                TextNode(" is last", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multi_image_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) plus a ![luke skywalker image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) is last")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" plus a ", TextType.TEXT, None),
                TextNode("luke skywalker image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" is last", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multi_link_to_textnodes(self):
        new_nodes = text_to_textnodes("[abe](https://abecodes.com) This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) plus a ![luke skywalker image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) is last")
        self.assertListEqual(
            [
                TextNode("abe", TextType.LINK, "https://abecodes.com"),
                TextNode(" This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" plus a ", TextType.TEXT, None),
                TextNode("luke skywalker image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" is last", TextType.TEXT),
            ],
            new_nodes,
        )