import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#it would be a lot smarter to compare the distance to the last used structure
#rather than to the previous structure
#e.g. imagine for every step the difference would be constant
#and the threshold is above that step
#also this way the first structure would not be rejected because of nan

def reduce_redundancy(data, metric, threshold, norm="max"):
    """
    This function takes in a dataframe already suitable for pacemaker
    and returns a dataframe that filters out all values of the metric that
    correspond to the threshold

    :param data: input data
    :param metric: can be "energy", "forces", "distance", "energy_corrected"
    :param threshold: if below the threshold structures are chosen to be too similar
    :param norm: in case of forces and distance can be "euclid", "frob", or "max"
    :return: a filtered dataset
    """

    if(metric == "energy"):
        differences = data["energy"].diff() #get energy differences between steps (1st is nan)

    if(metric == "energy_corrected"):
        differences = data["energy_corrected"].diff() #get energy differences between steps (1st is nan)

    if(metric == "forces"):
        #implement different norms
        differences = data['forces'].diff().apply(lambda x: np.linalg.norm(x, ord=norm))

    if(metric == "distance"):
        diff_pos = [data['ase_atoms'][i].positions - data['ase_atoms'][i - 1].positions
                 for i in range(1, len(data))]
        differences = np.linalg.norm(diff_pos, ord=norm, axis=(1, 2))

    #check if they are above the threshold
    indices = np.where(np.abs(differences) > threshold)[0]

    #return new dataset
    return data.iloc[indices]


if __name__ == '__main__':
    df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config9_rlx_at35_E14.75_b0_a0.pckl.gzip", compression="gzip")
    data_filterd=reduce_redundancy(df, "energy_corrected", 0.1)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("energy_corrected: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    col="k"
    plt.scatter(df.index.values, df["energy_corrected"], marker=".", s=0.8)
    plt.scatter(data_filterd.index.values, data_filterd["energy_corrected"], marker=".", s=0.8, color=col)
    plt.show()


    #for forces 0.3?
    norm=None
    data_filterd=reduce_redundancy(df, "forces", 1.3,norm=norm)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("Forces: Data was reduced to {:.2f}% ".format(reducion_degree*100))

    forces_frob_norm = df['forces'].apply(lambda x : np.linalg.norm(x, ord=norm))
    forces_frob_norm_reduced = data_filterd["forces"].apply(lambda x: np.linalg.norm(x, ord=norm))
    plt.scatter(forces_frob_norm.index.values, forces_frob_norm, marker=".", s=0.8)
    plt.scatter(forces_frob_norm_reduced.index.values, forces_frob_norm_reduced, marker=".", s=0.8, color=col)
    plt.show()


    norm=None
    data_filterd=reduce_redundancy(df, "distance", 0.046, norm=norm)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("Distance: Data was reduced to {:.2f}% ".format(reducion_degree*100))

    positions = [row['ase_atoms'].positions for index, row in df.iterrows()]
    frob_pos = np.linalg.norm(positions, ord='fro', axis=(1,2))

    positions_reduced = [(row_index, row_data['ase_atoms'].positions) for row_index, row_data in data_filterd.iterrows()]
    positions_reduced = pd.DataFrame(positions_reduced, columns=['index', 'ase_atoms'])
    frob_pos_reduced = positions_reduced["ase_atoms"].apply(lambda x: np.linalg.norm(x, ord='fro'))

    plt.scatter(np.linspace(0,len(frob_pos),len(frob_pos)), frob_pos, marker=".", s=0.8)
    plt.scatter(positions_reduced["index"], frob_pos_reduced, marker=".", s=0.8, color=col)
    plt.show()
