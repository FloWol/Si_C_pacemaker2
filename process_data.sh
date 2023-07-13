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
}

# Specify the folder path
folder="Data//multi_trajectories_Si/displacements/test/Si_config1_rlx_at48_E17.5_b0_a0.traj"

# Start traversing the main folder and its subfolders
traverse_folders "$folder"
