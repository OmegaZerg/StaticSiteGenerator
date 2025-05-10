from os.path import join, exists, isfile, isdir
from os import listdir, mkdir
from generate_pages import generate_page, generate_pages_recursive
import sys
import shutil
import logging
#!Note: This logger function will write out to 'main.log' each time it is called from this file. This will override the previous log file, which is fine for this application since all we care about is what happened on the more recent run and less concerned with generating historcal logs for this.
logging.basicConfig(level=logging.INFO, filename="main.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

#Helper function that will copy a source directory and everything it contains.
def copy_source(source_directory, destination_directory):
    if not source_directory:
        return
    contents = listdir(source_directory)
    logging.info(f"Contents found at source directory: {contents}")
    for item in contents:
        source_path = join(source_directory, item)
        destination_path = join(destination_directory, item)
        if isfile(source_path):
            logging.info(f"File found! Copying {item} from <{source_path}> to <{destination_path}>")
            shutil.copy(source_path, destination_path)
        elif isdir(source_path):
            logging.info(f"Directory found! First creating source directory...")
            try:
                mkdir(destination_path)
                logging.info("Directory created!")
            except FileExistsError as e:
                logging.info(f"Exception thrown: unable to create directory. Reason: {e}")
                sys.exit()
            logging.info(f"Performing black hole recursion...")
            copy_source(source_path, destination_path)
    logging.info("Checking to see if we made it out ok...")
    


#Function that copies all the contents from a source directory to a destination directory
#!Warning: This function will delete all contents of the destination directory prio to the move

def move_directory(source, destination):
    check_path = (exists(source), exists(destination))
    logging.info(f"source exists: {check_path[0]} ||destination exists: {check_path[1]}")
    if False in check_path:
        logging.info(f"Either the source or destination is invalid, exiting...")
        sys.exit()

    logging.info(f"Attempting to clear destination directory <{destination}>")
    try:
        shutil.rmtree(destination)
    except FileNotFoundError as e:
        logging.info(f"Exception thrown: unable to delete directory. Reason: {e}")
        sys.exit()

    logging.info(f"Deletion event completed on the <{destination}> directory.")
    logging.info(f"Is the destination still there after deletion? {exists(destination)}")

    logging.info(f"Attempting to copy from <{source}>")
    logging.info(f"Creating new directory <{destination}>...")
    try:
        mkdir(destination)
    except FileExistsError as e:
        logging.info(f"Exception thrown: unable to create directory. Reason: {e}")
        sys.exit()

    if not exists(destination):
        logging.info(f"Destination directory failed to be created!")
    logging.info(f"Destination directory <{destination}> was successfully created!")
    copy_source(source, destination)



def main():
    move_directory("static", "docs")
    #generate_page("content/index.md", "template.html", "public/index.html")
    #generate_pages_recursive("content", "template.html", "public")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
