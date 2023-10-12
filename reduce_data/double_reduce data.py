import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gzip
import time
from reduce_data_accurate import reduce_redundancy
from sample_more_peaks import reduce_redundancy_min_max





if __name__ == '__main__':
    df = pd.read_pickle("../data_grouped/Si_config9_rlx_at35_E15.25_b0_a0.pckl.gzip", compression="gzip")

    norm=None
    col="r"

    data_filterd =reduce_redundancy_min_max(df, "forces", 0.8,norm=norm)
    reducion_degree = data_filterd.shape[0] / df.shape[0]
    data_filterd = df.iloc[data_filterd]
    print("Forces Peak: Data was reduced to {:.2f}% ".format(reducion_degree*100))

    data_filterd = reduce_redundancy(data_filterd, "forces", 50, norm=norm, every_xth=4)
    reducion_degree = data_filterd.shape[0] / df.shape[0]
    print("Forces: Data was reduced to {:.2f}% ".format(reducion_degree * 100))

    forces_frob_norm = df['forces'].apply(lambda x : np.linalg.norm(x, ord=norm))
    forces_frob_norm_reduced = data_filterd["forces"].apply(lambda x: np.linalg.norm(x, ord=norm))
    plt.scatter(forces_frob_norm.index.values, forces_frob_norm, marker=".", s=0.8)
    plt.scatter(forces_frob_norm_reduced.index.values, forces_frob_norm_reduced, marker=".", s=0.8, color=col)
    plt.show()


