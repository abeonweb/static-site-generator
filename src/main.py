from textnode import TextNode, TextType
from inline_markdown import *
from block_markdown import *
from utils import copy_dir, extract_title, generate_pages_recursive

def main():
    copy_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()