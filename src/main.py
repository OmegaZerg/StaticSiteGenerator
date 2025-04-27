from os.path import join, exists, isfile
from os import listdir, mkdir
import sys
import shutil
import logging
logging.basicConfig(level=logging.INFO, filename="main.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

#Helper function that will copy a source directory and everything it contains.
def copy_source(source_directory, destination_directory):
    logging.info(f"Creating new directory < {destination_directory} >...")
    try:
        mkdir(destination_directory)
    except FileExistsError as e:
        logging.info(f"Exception thrown: unable to create directory. Reason: {e}")
        sys.exit()

    if not exists(join(destination_directory)):
        logging.info(f"Destination directory failed to be created!")
    logging.info(f"Destination directory < {destination_directory} > was successfully created!")

    contents = listdir(source_directory)
    logging.info(f"Contents found at source directory: {contents}")

#Function that copies all the contents from a source directory to a destination directory
#!Warning: This function will delete all contents of the destination directory prio to the move
"""
TODO: 1. Check the input destination/source paths are valid
TODO: 2. Clear destination directory
TODO: 3. Create helper function that logs each copy action
TODO: 4. Copy source directory and all contents to the destination directory
"""
def move_directory(source, destination):
    check_path = (exists(join(source)), exists(join(destination)))
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

    logging.info(f"Attempting to copy from < {source} >")
    copy_source(source, destination)



def main():
    move_directory("static", "test")

main()
