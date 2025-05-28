import unittest
from block_markdown import *

class BlockMarkdownTest(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_ordered(self):
        block="1. The\n2. start\n3. of\n4. something\n5. special"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_quote_error(self):
        block=">This is code\n>another line in quote\n>Nothing to see here"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_quote_error(self):
        block=""">This is code\n>another line in quote\n suspicious line in quote"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            html
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_lists(self):
        md = """
- Cheese\n- Bread\n- Milk\n

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ul><li>Cheese</li><li>Bread</li><li>Milk</li></ul></div>",
            html
        )

    def test_ordered_list(self):
        md = """
1. Cheese\n2. Bread\n3. Milk\n

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ol><li>Cheese</li><li>Bread</li><li>Milk</li></ol></div>",
            html
        )


    def test_heading(self):
        md="""
# h1 heading

#### h4 heading

###### h6 heading

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><h1>h1 heading</h1><h4>h4 heading</h4><h6>h6 heading</h6></div>",
            html
        )