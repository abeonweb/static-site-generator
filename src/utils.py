from os import listdir, mkdir, path
from shutil import rmtree, copy
import re
from block_markdown import markdown_to_html_node

def copy_dir(source, dest):
    # check if exists and delete destination dir
    if path.exists(dest):
        rmtree(dest)
    mkdir(dest)
    # for each item in source if dir, call copy_dir, else copy file
    dir_content = listdir(source)
    for item in dir_content:
        path_to= path.join(source, item)
        to_dest= path.join(dest, item)
        if not path.isfile(path_to):
            mkdir(to_dest)
            copy_dir(path_to, to_dest)
        else:
            copy(path_to, to_dest)

def extract_title(markdown):
    md_split=markdown.split("\n")
    match = re.fullmatch(r"(^# .+)", md_split[0])
    if match == None or len(match.group(0)) < 3:
        raise Exception("No title")
    else:
        title = match.group(0)
        title = title.strip("# ").rstrip()
        if len(title) < 1:
            raise Exception("No title")
        return title
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    f= open(from_path)
    md= f.read()
    html_node = markdown_to_html_node(md)
    content = html_node.to_html()
    title = extract_title(md)
    f2= open(template_path)
    template= f2.read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    
    f.close()
    f2.close()
    # check if dir exist
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir=listdir(dir_path_content)
    for item in dir:
        # create paths
        path_to_file = path.join(dir_path_content, item)
        to_dest = path.join(dest_dir_path, item)
       
        # check if md file 
        if(path.isfile(path_to_file)):
            # generate page and return
            generate_page(path_to_file, template_path, f"{dest_dir_path}/index.html")

        else: 
            # check and delete existing dir
            if path.exists(to_dest):
                rmtree(to_dest)
            mkdir(to_dest)
            generate_pages_recursive(path_to_file, template_path, to_dest)