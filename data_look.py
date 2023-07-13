import pandas as pd
import os
import gzip
import gc
import time
"""
This script fuses several smaller .gzips into on big gzip.
use create_dataset.py first and store in the source_dir folder
this might be needed for the data to fit into memory
"""
print("Starting ...")
source_dir="/home/flo/pacemaker/dataset"
dataset = pd.DataFrame(columns=['energy', 'forces', 'ase_atoms', 'energy_corrected'])
start_time = time.time()
for root, _, files in os.walk(source_dir):
    for file in files:
        print("processing file:" + str(file))
        if file.endswith(".pckl.gzip"):
            file_path = os.path.join(root, file)
            with gzip.open(file_path, "rb") as f:
                sub_dataset = pd.read_pickle(f)
                # check if they have the same data format
                if set(dataset.columns) == set(sub_dataset.columns):
                    dataset = pd.concat([dataset, sub_dataset], ignore_index=True)
                    # do redundancy sampling
            f.close()
        gc.collect()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

print("pickeling data ...")
dataset.to_pickle("final_dataset.pckl.gzip", compression='gzip', protocol=4)

print(dataset.head())
print(dataset.tail())
print("done")


#does the order matter?
#files are not processed in order
##https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#concatenating-objects
# look at the link to make things more efficient