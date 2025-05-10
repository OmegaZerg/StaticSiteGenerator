
#TODO 1: extract title should pull the h1 header from markdown file input and return it.
#TODO 2: Write unit tests for extract title
#TODO 3: generate page should print message, read markdown file from provided path, read template from path, use several other functions to write out a full html page at destinatino path.

#Function that will take a markdown document as input and return the h1 header from the file (markdown and leading/trailing whitespace are stripped out). If no h1 header is found then an exception will be thrown.

def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line
            break
    title.lstrip("#").strip()
    if not title:
        raise Exception("Error: No title(h1 header) found in provided markdown document")
    else:
        return title
    
