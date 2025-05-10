from markdown_blocks import markdown_to_html_node
import shutil
from os.path import dirname, join, exists, isfile, isdir, splitext
from os import listdir, mkdir, makedirs
import sys
import logging
logging.basicConfig(level=logging.INFO, filename="generate_pages.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")


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
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not dir_path_content:
        return
    contents = listdir(dir_path_content)
    logging.info(f"Contents found at source directory: {contents}")
    for item in contents:
        source_path = join(dir_path_content, item)
        destination_path = join(dest_dir_path, item)
        if isfile(source_path):
            root, ext = splitext(destination_path)
            if ext == ".md":
                html_file = root + ".html"
                logging.info(f"Markdown file found! Copying {item} from <{source_path}> to <{html_file}>")
                generate_page(source_path, template_path, html_file)
            else:
                logging.info(f"{ext} file type found, this file type is not accepted currently...skipping file.")
                
        elif isdir(source_path):
            logging.info(f"Directory found! First creating source directory...")
            try:
                mkdir(destination_path)
                logging.info("Directory created!")
            except FileExistsError as e:
                logging.info(f"Exception thrown: unable to create directory. Reason: {e}")
                sys.exit()
            logging.info(f"Performing black hole recursion...")
            generate_pages_recursive(source_path, template_path, destination_path)
    logging.info("Checking to see if we made it out ok...")