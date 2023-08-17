import pandas as pd
import gzip
import os
import gc
import time
"""
Same as data_look but a lot faster, maybe more memory inefficient

This script fuses several smaller .gzips into on big gzip.
use create_dataset.py first and store in the source_dir folder
this might be needed for the data to fit into memory
"""


def process_files(file, root):
    columns = ['energy', 'forces', 'ase_atoms', 'energy_corrected']
    print("processing file:" + str(file))
    if file.endswith(".pckl.gzip"):
        file_path = os.path.join(root, file)
        with gzip.open(file_path, "rb") as f:
            sub_dataset = pd.read_pickle(f)
            # check if they have the same data format
            if set(columns) == set(sub_dataset.columns):
                sub_dataset["energy"] = sub_dataset["energy"].astype("float32")
                sub_dataset["energy_corrected"] = sub_dataset["energy_corrected"].astype("float32")
                return sub_dataset
        f.close()

source_dir = "/home/flo/pacemaker/dataset"
dataset = pd.DataFrame(columns=['energy', 'forces', 'ase_atoms', 'energy_corrected'])
start_time = time.time()
for root, _, files in os.walk(source_dir):
    frames = [ process_files(file, root) for file in files ]
result = pd.concat(frames)
gc.collect()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

result.to_pickle("final_dataset.pckl.gzip", compression='gzip', protocol=4)