from htmlnode import LeafNode
from textnode import TextNode, TextType
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text_node.text)
        case TextType.BOLD:
            return LeafNode("b",text_node.text)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text)
        case TextType.CODE:
            return LeafNode("code",text_node.text)
        case TextType.LINK:
            return LeafNode("a",text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, {"src":text_node.url, "alt":text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # each old node has text
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_list= node.text.split(delimiter)
        # print("Valid", "|node.text: ",node.text, "|text_list", text_list, "delim", delimiter,"\n")
        if len(text_list) % 2 == 0:
            # print("Invalid", "|node.text: ",node.text, "|text_list", text_list, "delim", delimiter,"\n")
            raise Exception("Invalid markdown syntax")    
        for i in range(len(text_list)):
            if text_list[i] == "":
                continue
            if i % 2 == 0:
                textnode= TextNode(text_list[i], TextType.TEXT)
                new_nodes.append(textnode)
            else:
                textnode= TextNode(text_list[i], text_type)
                new_nodes.append(textnode)
    return new_nodes 

def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)

def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)

def split_nodes_image(old_nodes):
    new_nodes=[]
    # each node in list split. 
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if len(extracted_images) < 1:
            new_nodes.append(node)
            continue
        updated_str=node.text
        for image in extracted_images:
            text, rest = updated_str.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            updated_str = rest
        if len(updated_str) > 0:
            new_nodes.append(TextNode(updated_str, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes=[]
    # each node in list split. 
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if len(extracted_links) < 1:
            new_nodes.append(node)
            continue
        updated_str=node.text
        for link in extracted_links:
            text, rest = updated_str.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            if len(text) > 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            updated_str = rest
        # done extracting links, add remaining text node
        if len(updated_str) > 0:
            new_nodes.append(TextNode(updated_str, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_strip=text.replace("\n"," ")
    # turn text into a text node
    text_node = TextNode(text_strip, TextType.TEXT)
    new_nodes=split_nodes_delimiter([text_node], "**", TextType.BOLD)
    new_nodes=split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes=split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    nodes_after_images=split_nodes_image(new_nodes)
    nodes_after_links=split_nodes_link(nodes_after_images)
    return nodes_after_links