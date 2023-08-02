import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


def reduce_redundancy(df, metric, threshold, norm=None, full_return=False):
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


    index_dict = {
        "energy" : 1,
        "forces" : 2,
        "distance" : 3,
        "energy_corrected" : 4
    }

    last_taken = 0
    df['Difference'] = 0
    diff_function = get_diff_func(metric, norm)

    #in case the metric is positions we have to take care of  FIXME
    #first iteration to make sure the first value is included
    if(metric == "distance"):
        last_taken = df["ase_atoms"].iloc[0]
        df.loc[0, 'Difference'] = threshold+0.1

    step = 0
    # Iterate over the DataFrame rows using itertuples
    for row in df.itertuples(index=True):
        step += 1
        current_value = row[index_dict[metric]]
        difference = diff_function(last_taken, current_value)
        #df.loc[row[0], 'Difference'] = difference #not good FIXME

        # Check if the difference exceeds the threshold
        if abs(difference)/step > threshold:
            df.loc[row[0], 'Difference'] = difference  #not good FIXME
            # Update the last taken value
            last_taken = current_value
            step = 0

    if(full_return):
        return df
    else:
        return df[np.abs(df["Difference"]) > threshold].iloc[:, :4]#.reset_index(drop=True)



def plot_df(energy_df):
    #plt.scatter(np.linspace(0,len(energy_df),len(energy_df)), energy_df, marker=".", s=0.8)
    plt.scatter(energy_df.index.values, energy_df, marker=".", s=0.8)
    plt.show()

if __name__ == '__main__':
    df = pd.read_pickle("/data_grouped/Si_config9_rlx_at35_E14.75_b0_a0.pckl.gzip", compression="gzip")
    data_filterd=reduce_redundancy(df, "energy_corrected", 0.02)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    col="m"
    print("energy_corrected: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    plt.scatter(df.index.values, df["energy_corrected"], marker=".", s=0.8)
    plt.scatter(data_filterd.index.values, data_filterd["energy_corrected"], marker=".", s=0.8)
    plt.show()


    #for forces 0.3?
    norm="fro"
    data_filterd=reduce_redundancy(df, "forces", 0,norm=norm)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("Forces: Data was reduced to {:.2f}% ".format(reducion_degree*100))

    forces_frob_norm = df['forces'].apply(lambda x : np.linalg.norm(x, ord=norm))
    forces_frob_norm_reduced = data_filterd["forces"].apply(lambda x: np.linalg.norm(x, ord=norm))
    plt.scatter(forces_frob_norm.index.values, forces_frob_norm, marker=".", s=0.8)
    plt.scatter(forces_frob_norm_reduced.index.values, forces_frob_norm_reduced, marker=".", s=0.8)
    plt.show()


    norm="fro"
    data_filterd=reduce_redundancy(df, "distance", 0.0001, norm=norm)
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

