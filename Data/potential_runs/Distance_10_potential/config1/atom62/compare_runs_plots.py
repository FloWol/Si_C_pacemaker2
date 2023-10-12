import os
import numpy as np
import matplotlib.pyplot as plt
from ase import io
import pandas as pd

def plot_compare(md_path, pace_path):
    traj_md = io.Trajectory(md_path, 'r')
    pace_md = io.Trajectory(pace_path, 'r')

    def get_vals(images):
        data = {'energy': [],
                'forces': []}

        for i in range(len(images)):
            im = images[i]

            pe = im.get_potential_energy()

            data['energy'].append(pe)
            data['forces'].append(im.get_forces())

        return pd.DataFrame(data)

    md_data = get_vals(traj_md)
    pace_data = get_vals(pace_md)

    plt.scatter(md_data.index.values, md_data["forces"].apply(lambda x: np.linalg.norm(x)), marker=".", s=0.8,
                label="MD")
    plt.scatter(pace_data.index.values, pace_data["forces"].apply(lambda x: np.linalg.norm(x)), marker=".", s=0.8,
                label="ML")
    plt.legend()
    plt.title(md_path)
    plt.show()



folder_path = "/home/flo/pacemaker/Data/potential_runs/Distance_10_potential/config1/atom62"
# List all files in the folder
file_list = os.listdir(folder_path)

# Create a dictionary to group files by their base name (without "_pot" or "_atXX")
file_groups = {}
for file_name in file_list:
    base_name = file_name.replace("_pot", "").replace("_at", "_")
    if base_name not in file_groups:
        file_groups[base_name] = []
    file_groups[base_name].append(file_name)

# Iterate through each group and execute the desired function
for base_name, files in file_groups.items():
    if len(files) == 2:  # Ensure there is a pair of files for each group
        file1, file2 = files
        if "pot" in file1:
            pace_path = file1
            md_path = file2
        else:
            md_path = file1
            pace_path = file2
        # Extract the numbers after "E" from the file names

        # Execute your function using the file names and extracted numbers
        plot_compare(md_path, pace_path)
