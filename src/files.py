import pathlib
import os
import shutil
from markdown_to_node import markdown_to_html_node



def copy_dir(source_path, destination_path):
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    
    if not os.path.isdir(source_path):
        shutil.copy(src= source_path, dst= destination_path)
    else:
        os.mkdir(destination_path)
        list_path = os.listdir(source_path)
        for path in list_path:
            copy_dir(source_path= os.path.join(source_path,path) ,destination_path=os.path.join(destination_path, path))

def extract_header(markdown:str):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line.strip("# ")

    raise Exception("Doesnt contain header")

def generate_page(from_path, template_path, dest_path):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template: str = file.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_header(markdown)
    half_html = template.replace("{{ Content }}", html_string)
    full_html = half_html.replace("{{ Title }}", title)
    path = pathlib.Path(dest_path.replace(".md", ".html"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as file:
        file.write(full_html)

def generate_pages_recursive(source_path, template_path, destination_path):
    if os.path.isfile(source_path):
        if os.path.isdir(destination_path):
            generate_page(source_path,template_path,os.path.join(destination_path,source_path))
        generate_page(source_path,template_path,destination_path)
        return

    for file in os.listdir(source_path):
        generate_pages_recursive(os.path.join(source_path,file), template_path, os.path.join(destination_path,file))
