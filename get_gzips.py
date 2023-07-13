import os
import shutil

"""
This script searches for .pckl.gzip files in the source directory
and creates a similar structured destination folder that includes the 
gzip and only the gzip folders.
"""
def copy_pckl_gzip_files(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".pckl.gzip"):
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_file_path, source_dir)
                destination_file_path = os.path.join(destination_dir, relative_path)
                destination_folder = os.path.dirname(destination_file_path)

                os.makedirs(destination_folder, exist_ok=True)
                shutil.copy2(source_file_path, destination_file_path)
                print(f"Copied {source_file_path} to {destination_file_path}")

source_directory = "/home/flo/pacemaker/Data"
destination_directory = "home/flo/pacemaker/Data_gzip"

copy_pckl_gzip_files(source_directory, destination_directory)