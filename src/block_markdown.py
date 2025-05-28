from enum import Enum
import re
from htmlnode import *
from inline_markdown import text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"


def markdown_to_blocks(markdown):
    break_to_lines = markdown.split("\n\n")
    after_strip = list(map(lambda item: item.strip(), break_to_lines))
    after_filter_extra_newlines = list(filter(lambda item: len(item)> 0, after_strip))
    return after_filter_extra_newlines

def block_to_block_type(block):
    if block =="" or block == None:
        return
    regex = r"(^#{1,6} ).+?"
    if re.fullmatch(regex, block):
        return BlockType.HEADING
    regex= r"^`{3}\n(.+\n){1,}`{3}$"
    if re.fullmatch(regex, block):
        return BlockType.CODE

    block_by_lines = block.splitlines()
    not_a_quote = list(filter(lambda i: not i.startswith(">"), block_by_lines))
    if len(not_a_quote) < 1:
        return BlockType.QUOTE
    not_a_list = list(filter(lambda i: not i.startswith("-"), block_by_lines))
    if len(not_a_list) < 1:
        return BlockType.UNORDERED_LIST
    numbers_in_list = list(map(lambda i: i.split(". ",maxsplit=1)[0], block_by_lines))
    if len(numbers_in_list) > 0:
        flag = True
        for i in range(0, len(numbers_in_list)):
            if numbers_in_list[i].isdigit() and (i+1 != int(numbers_in_list[i])) or not block_by_lines[i].startswith(f"{i+1}. "):
                flag = False
        if flag:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children
    
def block_type_to_node(type, block):
    if type == BlockType.CODE:
        strip_block = block[4:-3]
        text_node = TextNode(strip_block, TextType.TEXT)
        node = text_node_to_html_node(text_node)
        code = ParentNode("code", [node])
        return ParentNode("pre", [code])
    if block.startswith("#") and type == BlockType.HEADING:
        h_count = block.count("#")
        block=block.strip("#")
        block=block.strip(" ")
        children=text_to_children(block)
        return ParentNode(f"h{h_count}", children)
    lines=block.split("\n\n")
    children=[]
    if type == BlockType.QUOTE:
        line_quotes=block.split(">")
        for quote in line_quotes:
            value = quote.strip("> ")
            nodes = text_to_textnodes(value)
            children.append(LeafNode(None, value))
        return ParentNode("blockquote", children)
    if type == BlockType.UNORDERED_LIST:
        for item in block.split("\n"):
            value = item.strip("- ")
            text_nodes=text_to_textnodes(value)
            inner=[]
            for node in text_nodes:
                inner.append(text_node_to_html_node(node))
            children.append(ParentNode("li", inner))
        return ParentNode("ul", children)
    if type == BlockType.ORDERED_LIST:
        for item in block.split("\n"):
            value = item.split(" ", maxsplit=1)
            text_nodes=text_to_textnodes(value[1])
            inner=[]
            for node in text_nodes:
                inner.append(text_node_to_html_node(node))
            children.append(ParentNode("li", inner))
        return ParentNode("ol", children)
    # return a paragragh
    children = text_to_children(block)
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    children=[]
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_type_to_node(block_type, block)
        children.append(node)
    return ParentNode("div", children)