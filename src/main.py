from textnode import TextNode, TextType
from inline_markdown import *
from block_markdown import *
from utils import copy_dir, extract_title, generate_pages_recursive
import sys
def main():
    basepath=""
    if sys.argv[1]:
        basepath= sys.argv[1]
    else:
        basepath= "/"
    copy_dir("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()