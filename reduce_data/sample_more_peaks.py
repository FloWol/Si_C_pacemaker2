import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as signal

"""
This version is like reduce_data, but here we we compare it to the last structure taken and not 
the immediate difference between two rows
"""

#TODO implement difference by derivative
#like deltaE/stepsize 0.3 fs
#maybe preserve original plot structure

def get_diff_func(metric, norm):

    losses = {
        "energy": lambda x, y: x - y,
        "energy_corrected": lambda x, y: x - y,
        "forces": lambda x, y: np.linalg.norm(x-y, ord=norm),
        "distance": lambda x, y: np.linalg.norm(x.positions-y.positions, ord=norm)

    }

    return losses[metric]


def reduce_redundancy_min_max(df, metric, reduction, norm=None, boost_factor=2, peak_importance_factor=1000, full_return=False):
    """
    This function takes in a dataframe already suitable for pacemaker
    and returns a dataframe that filters out all values of the metric that
    correspond to the threshold

    :param data: input data
    :param metric: can be "energy", "forces", "distance", "energy_corrected"
    :param threshold: if below the threshold structures are chosen to be too similar
    :param norm: in case of forces and distance can be "frob", eclid and max are to be implemented, but max can be
                passed with np.inf
    :return: a filtered dataset
    """



    data=df[metric]
    data_len = len(data)

    if(metric=="forces"):
        data = df['forces'].apply(lambda x: np.linalg.norm(x, ord=norm))
    if(metric == "ase_atoms"):
        positions = [row['ase_atoms'].positions for index, row in df.iterrows()]
        data = np.linalg.norm(positions, ord=norm, axis=(1, 2))

    positive_peaks, _ = signal.find_peaks(data)
    negative_peaks, _ = signal.find_peaks(-data)

    # Step 3: Downsampling with Importance Weighting
    peaks = np.concatenate((positive_peaks, negative_peaks))
    peaks = np.sort(peaks)

    distances_to_peaks = np.min(np.abs(np.subtract.outer(np.arange(len(data)), peaks)), axis=1)
    importance_weights = 1.0 / (1.0 + distances_to_peaks)

    peak_importance_factor = 1.8  # You can adjust this factor as needed
    importance_weights[peaks] *= peak_importance_factor

    non_peak_downsampling_factor = 1  # You can adjust this factor as needed
    importance_weights[~np.isin(np.arange(len(data)), peaks)] *= non_peak_downsampling_factor

    # Normalize the importance weights to sum to 1
    importance_weights /= np.sum(importance_weights)


    downsampled_indices = np.random.choice(len(data), size=int(np.round(data_len*reduction)), replace=False,
                                           p=importance_weights)

    if(full_return):
        return downsampled_indices
    else:
        return downsampled_indices



def plot_df(energy_df):
    #plt.scatter(np.linspace(0,len(energy_df),len(energy_df)), energy_df, marker=".", s=0.8)
    plt.scatter(energy_df.index.values, energy_df, marker=".", s=0.8)
    plt.show()

if __name__ == '__main__':
    df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config9_rlx_at35_E14.75_b0_a0.pckl.gzip", compression="gzip")
    col = "r"
    # data_filterd=reduce_redundancy_weight(df, "energy_corrected", 0.21)
    # reducion_degree = data_filterd.shape[0]/df.shape[0]
    # print("energy_corrected: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    #
    # plt.scatter(df.index.values, df["energy_corrected"], marker=".", s=0.8)
    # plt.scatter(data_filterd, df["energy_corrected"][data_filterd], marker=".", s=0.8, color=col)
    # plt.show()



    norm="fro"
    data_filterd=reduce_redundancy_min_max(df, "forces", 0.3,norm=norm)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("Forces: Data was reduced to {:.2f}% ".format(reducion_degree*100))

    forces_frob_norm = df['forces'].apply(lambda x : np.linalg.norm(x, ord=norm))
    plt.scatter(forces_frob_norm.index.values, forces_frob_norm, marker=".", s=0.8)
    plt.scatter(data_filterd, forces_frob_norm[data_filterd], marker=".", s=0.8, color=col)
    plt.show()


    # norm=np.inf
    # data_filterd=reduce_redundancy_weight(df, "ase_atoms", 0.21, norm=norm)
    # reducion_degree = data_filterd.shape[0]/df.shape[0]
    # print("Distance: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    #
    # positions = [row['ase_atoms'].positions for index, row in df.iterrows()]
    # frob_pos = np.linalg.norm(positions, ord=norm, axis=(1,2))
    #
    # plt.scatter(np.linspace(0,len(frob_pos),len(frob_pos)), frob_pos, marker=".", s=0.8)
    # plt.scatter(data_filterd, frob_pos[data_filterd], marker=".", s=0.8, color=col)
    # plt.show()
