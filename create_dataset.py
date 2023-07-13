import os

import numpy as np
import pandas as pd
import gzip
import time
from reduce_data import reduce_redundancy
from pandas.core.nanops import set_use_bottleneck

"""
This script creates a pandas dataframe containing the data that can then be read by pacemaker
"""

def parameters(interactive=False):
    if (interactive):
        print("interactive")
    else:
        print("interactive")
    return
def create_dataframe():
    return


def concat_dataframes(root_folder,  metric, threshold):
    print("starting concatenating")
    start_time = time.time()


    #browse filesystem and add data to dataframe
    chunk=0
    for root, dirs, files in os.walk(root_folder):
        dataset = pd.DataFrame(columns=['energy', 'forces', 'ase_atoms', 'energy_corrected'])
        print("browsing: " + str(root))
        for file in files:
            if file.endswith(".pckl.gzip"):
                file_path = os.path.join(root, file)
                with gzip.open(file_path, "rb") as f:
                    sub_dataset = pd.read_pickle(f)
                #check if they have the same data format
                    if set(dataset.columns) == set(sub_dataset.columns):
                        sub_dataset = reduce_redundancy(sub_dataset, metric, threshold)
                        dataset=pd.concat([dataset, sub_dataset], ignore_index=True)
                        #do redundancy sampling

                f.close()
        chunk+=1
        dataset.to_pickle("dataset/"+str(chunk)+"dataset.pckl.gzip", compression='gzip', protocol=4)  # include destination

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

    return #dataset #commented to be easier on the memory


#if __name__ == '__main__':
single_Si = True
multi_Si = True
eV_range = lambda start, end, step=0.5: np.arange(start,end+step,step)



folder_path = "/home/flo/pacemaker/Data/"  # Replace with the actual root folder path
dataset = concat_dataframes(folder_path)
print("done")

