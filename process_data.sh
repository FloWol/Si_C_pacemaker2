#!/bin/bash

# Function to process files
process_file() {
    file="$1"
    if [ -f "$file" ]; then  # Check if the file exists
        echo "Processing file: $file"
        python ASE_to_Pacemaker_script.py "$file"
    fi
}

# Function to traverse folders recursively
traverse_folders() {
    folder="$1"
    for file in "$folder"/*; do
        if [ -d "$file" ]; then  # Check if it's a directory
            traverse_folders "$file"  # Recursive call for subfolder
        elif [[ "$file" == *.traj ]]; then  # Check if the file ends with ".traj"
            process_file "$file"
        fi
    done
    echo "Task completed successfully!"
}

# Specify the folder path
folder="/home/flo/pacemaker/Data/multi_Si"

# Start traversing the main folder and its subfolders
traverse_folders "$folder"
