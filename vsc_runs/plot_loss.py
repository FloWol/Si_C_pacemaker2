import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from astropy.table import Table

source_dir="/home/flo/pacemaker/vsc_runs"

for root, _, files in os.walk(source_dir):
    for file in files:
        if (file=="metrics.txt" or file=="test_metrics.txt"):
            file_path = os.path.join(root, file)
            print("processing file:" + str(file_path))
            frame=Table.read(file_path, format='ascii')
            # frame = pd.read_table(file_path,
            #                       sep=" ",
            #                       usecols="loss",
            #                       na_values=["NaN"]
            #                       )
            indices = np.argwhere(frame["iter_num"] > 50)
            plt.title(file_path)
            plt.plot(frame["iter_num"][indices], frame["loss"][indices], "-o",  markersize=4)

    plt.show()