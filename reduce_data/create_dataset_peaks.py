import os

import numpy as np
import pandas as pd
import gzip
import time

from sample_more_peaks  import reduce_redundancy_min_max
from pandas.core.nanops import set_use_bottleneck

"""
This script creates a pandas dataframe containing the data that can then be read by pacemaker
if used with group_data it creates one dataframe

if used with get_gzips it will creat a dataframe for every subfolder
    the last option might be better if memory is limited
    then use data_collection or data_look to unite the dataframe to one dataframe

"""


def parameters(interactive=False):
    if (interactive):
        print("interactive")
    else:
        print("interactive")
    return


def create_dataframe():
    return


def concat_dataframes(root_folder, metric, threshold,reduction_f, norm=None):
    print("starting concatenating")
    start_time = time.time()

    # browse filesystem and add data to dataframe
    chunk = 0
    for root, dirs, files in os.walk(root_folder):
        dataset = pd.DataFrame(columns=['energy', 'forces', 'ase_atoms', 'energy_corrected'])
        print("browsing: " + str(root))
        for file in files:
            try:
                if file.endswith(".pckl.gzip"):
                    file_path = os.path.join(root, file)
                    with gzip.open(file_path, "rb") as f:
                        sub_dataset = pd.read_pickle(f)
                        prefiltered_size = sub_dataset.shape[0]
                        # check if they have the same data format
                        if set(dataset.columns) == set(sub_dataset.columns):
                            sub_index = reduction_f(sub_dataset, metric, threshold,
                                                            norm)  # FIXME could be more efficient
                            sub_dataset = sub_dataset.iloc[sub_index]
                            dataset = pd.concat([dataset, sub_dataset], ignore_index=True)
                            # print reduction rate
                        reducion_degree = sub_dataset.shape[0] / prefiltered_size
                        print("energy_corrected: Data was reduced to {:.2f}% ".format(reducion_degree * 100))

                    f.close()
            except Exception as e:
                print(f"Error occurred while processing file: {file_path}")
                print(f"Error message: {str(e)}")
                continue

        chunk += 1
        dataset.to_pickle("/home/flo/pacemaker/dataset_reduced/"
                          + str(chunk) + "enitre_data" + metric + str(int(threshold * 10)) +
                          ".pckl.gzip", compression='gzip', protocol=4)  # include destination

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

    return  # dataset #commented to be easier on the memory


# if __name__ == '__main__':
single_Si = True
multi_Si = True
eV_range = lambda start, end, step=0.5: np.arange(start, end + step, step)

folder_path = "/home/flo/pacemaker/data_grouped" # Replace with the actual root folder path
concat_dataframes(folder_path, "forces", 0.6, reduce_redundancy_min_max, norm="fro")
print("done")

