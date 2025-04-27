from os.path import join, exists, isfile
import sys
import shutil
import logging
logging.basicConfig(level=logging.INFO, filename="main.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

#Function that copies all the contents from a source directory to a destination directory
#!Warning: This function will delete all contents of the destination directory prio to the move
"""
TODO: 1. Check the input destination/source paths are valid
TODO: 2. Clear destination directory
TODO: 3. Create helper function that logs each copy action
TODO: 4. Copy source directory and all contents to the destination directory
"""
def move_directory(source, destination):
    test_source = join(source)
    logging.info(f"source format: {test_source}")
    test_destination = join(destination)
    logging.info(f"destination format: {test_destination}")
    check_path = (exists(test_source), exists(test_destination))
    logging.info(f"source exists: {check_path[0]} ||destination exists: {check_path[1]}")
    logging.info(f"attempting to clear destination directory <{destination}>")
    try:
        shutil.rmtree(destination)
    except FileNotFoundError as e:
        logging.info(f"Exception thrown: unable to delete directory. Reason: {e}")
        sys.exit()

    logging.info(f"Deletion event completed on the<{destination}> directory.")
    check_destination = exists(destination)
    logging.info(f"Is the destination still there after deletion? {check_destination}")



def main():
    move_directory("static", "test")

main()
