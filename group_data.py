import os
import shutil
import sys

"""
This script takes all .pckl.gzip files and copies them to a single folder
"""
def copy_pickl_gzip_files(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Recursively search for files ending with ".pickl.gzip" in the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".pckl.gzip"):
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_dir, file)
                shutil.copy2(source_file, destination_file)

    print("Files copied successfully.")

# Define the source directory to search for files
source_dir = sys.argv[1] #"/home/flo/pacemaker/Data/multi_Si"

# Define the destination directory to copy the files
destination_dir = sys.argv[2]#'/home/flo/pacemaker/data_grouped'

copy_pickl_gzip_files(source_dir, destination_dir)
