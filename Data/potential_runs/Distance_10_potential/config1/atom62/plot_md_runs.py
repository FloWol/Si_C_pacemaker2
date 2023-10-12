import os
import numpy as np
import matplotlib.pyplot as plt
from ase import io
import pandas as pd

def plot_compare(pace_path):
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

    pace_data = get_vals(pace_md)
    plt.scatter(pace_data.index.values, pace_data["forces"].apply(lambda x: np.linalg.norm(x)), marker=".", s=0.8,
                label="ML")
    plt.legend()
    plt.title(pace_path)
    plt.show()



folder_path = "/home/flo/pacemaker/Data/potential_runs/Distance_10_potential/config1/atom62"
# List all files in the folder
file_list = os.listdir(folder_path)
file_names = sorted([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])

# Create a dictionary to group files by their base name (without "_pot" or "_atXX")
file_groups = {}
for name in file_names:
    if "pot" in name:
        if name.endswith(".traj"):
            print(name)
            plot_compare(name)
