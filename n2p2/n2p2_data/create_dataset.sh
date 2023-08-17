#!/bin/bash
#Short bash script that allows to combine all the .data files within a folder

input_folder="/home/flo/pacemaker/n2p2/n2p2_data"  # Replace with the actual path to your folder
output_file="input.data"   # Replace with the desired output file name

for file in "$input_folder"/*.data; do
    echo  "$file"
    cat "$file" >> "$output_file"
    echo >> "$output_file"  # Add a newline between file contents
done
