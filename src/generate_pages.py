from markdown_blocks import markdown_to_html_node
import shutil
from os.path import dirname, join, exists, isfile, isdir
from os import listdir, mkdir, makedirs
import sys
import logging
logging.basicConfig(level=logging.INFO, filename="generate_pages.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
#TODO 3: generate page should print message, read markdown file from provided path, read template from path, use several other functions to write out a full html page at destinatino path.

#Function that will take a markdown document as input and return the h1 header from the file (markdown and leading/trailing whitespace are stripped out). If no h1 header is found then an exception will be thrown.

def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        clean = line.strip()
        if clean.startswith("# "):
            title = clean
            break
    if not title:
        raise Exception("Error: No title(h1 header) found in provided markdown document")
    else:
        final = title.lstrip("# ").strip()
        return final
    
def generate_page(from_path, template_path, dest_path):
    logging.info(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    logging.info(f"Opening file at: {from_path}")
    with open(from_path, "r") as file:
        md_content = file.read()
    logging.info(f"Opening template file at: {template_path}")
    with open(template_path, "r") as file:
        template = file.read()
        lines = template.split("\n")
    logging.info(f"Creating HTML Node from markdown file...")
    html_node = markdown_to_html_node(md_content)
    logging.info(f"Creating HTML string from node object using to_html method...")
    page_content = html_node.to_html()
    logging.info(f"Extracting page title from markdown file...")
    page_title = extract_title(md_content)
    logging.info(f"Reading html template file at {template_path} and replacing TITLE and CONTENT with the content we just extracted from the markdown file. Already opened and stored this in the template and lines variables above.")
    new_html = ""
    for line in lines:
        if "{{ Title }}" in line:
            new_line = line.replace("{{ Title }}", page_title)
        elif "{{ Content }}" in line:
            new_line = line.replace("{{ Content }}", page_content)
        else:
            new_line = line
        new_html = new_html + new_line + "\n"
    
    logging.info(f"Writing new HTML page to {dest_path}...")
    dest_dir = dirname(dest_path)
    if dest_dir and not exists(dest_dir):
        makedirs(dest_dir)
    with open(dest_path, 'w') as f:
        f.write(new_html)
    

    