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


def reduce_redundancy(df, metric, threshold, norm=None, every_xth=5):
    """
    This function takes in a dataframe already suitable for pacemaker
    and returns a dataframe that filters out all values of the metric that
    correspond to the threshold.
    It works by comparing the last taken value to the next one.
    If the value is not taken (difference is lower than threshhold) it will again compare the last
    taken value to the one after that.
    If a value is taken it will be the new last taken value that is used to compare the upcoming values to.


    :param data: input data
    :param metric: can be "energy", "forces", "distance", "energy_corrected"
    :param threshold: if below the threshold structures are chosen to be too similar
    :param norm: in case of forces and distance can be "fro", or np.inf for max norm
    :param full_return: return full dataset with differences if full_return = True
    :param every_xth: if the threshold is not met for x steps take the x+1 value. If set to 0 this is ignored
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
    consecutive_below_threshold = 0
    selected_indices = []

    #in case the metric is positions we have to take care of  TODO
    #first iteration to make sure the first value is included
    if(metric == "distance"):
        last_taken = df["ase_atoms"].iloc[0]
        df.loc[0, 'Difference'] = threshold+0.1

    # Iterate over the DataFrame rows using itertuples
    for row in df.itertuples(index=True):
        current_value = row[index_dict[metric]]
        difference = diff_function(last_taken, current_value)
        #df.loc[row[0], 'Difference'] = difference #TODO

        # Check if the difference exceeds the threshold
        if abs(difference) > threshold:
            selected_indices.append(row.Index)  #TODO
            # Update the last taken value
            last_taken = current_value
            consecutive_below_threshold = 0

        elif consecutive_below_threshold > every_xth: #every xth step do it anyway
            selected_indices.append(row.Index)
            last_taken = current_value
            consecutive_below_threshold = 0
        elif every_xth == 0:
            continue
        else:
            consecutive_below_threshold += 1



    return df.iloc[selected_indices].drop(columns="Difference")



def plot_df(energy_df):
    #plt.scatter(np.linspace(0,len(energy_df),len(energy_df)), energy_df, marker=".", s=0.8)
    plt.scatter(energy_df.index.values, energy_df, marker=".", s=0.8)
    plt.show()

if __name__ == '__main__':
    df = pd.read_pickle("../data_grouped/Si_config9_rlx_at35_E14.75_b0_a0.pckl.gzip", compression="gzip")
    # data_filterd=reduce_redundancy(df, "energy_corrected", 0.2)
    # reducion_degree = data_filterd.shape[0]/df.shape[0]
    # print("energy_corrected: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    col="r"
    # plt.scatter(df.index.values, df["energy_corrected"], marker=".", s=0.8)
    # plt.scatter(data_filterd.index.values, data_filterd["energy_corrected"], marker=".", s=0.8, color=col)
    # plt.show()


    #for forces 0.3?
    norm="fro"
    data_filterd=reduce_redundancy(df, "forces", 2.5,norm=norm, every_xth=5)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("Forces: Data was reduced to {:.2f}% ".format(reducion_degree*100))

    forces_frob_norm = df['forces'].apply(lambda x : np.linalg.norm(x, ord=norm))
    forces_frob_norm_reduced = data_filterd["forces"].apply(lambda x: np.linalg.norm(x, ord=norm))
    plt.scatter(forces_frob_norm.index.values, forces_frob_norm, marker=".", s=0.8)
    plt.scatter(forces_frob_norm_reduced.index.values, forces_frob_norm_reduced, marker=".", s=0.8, color=col)
    plt.show()


    # norm=np.inf
    # data_filterd=reduce_redundancy(df, "distance", 0.4, norm=norm)
    # reducion_degree = data_filterd.shape[0]/df.shape[0]
    # print("Distance: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    #
    # positions = [row['ase_atoms'].positions for index, row in df.iterrows()]
    # frob_pos = np.linalg.norm(positions, ord=norm, axis=(1,2))
    #
    # positions_reduced = [(row_index, row_data['ase_atoms'].positions) for row_index, row_data in data_filterd.iterrows()]
    # positions_reduced = pd.DataFrame(positions_reduced, columns=['index', 'ase_atoms'])
    # frob_pos_reduced = positions_reduced["ase_atoms"].apply(lambda x: np.linalg.norm(x, ord=norm))
    #
    # plt.scatter(np.linspace(0,len(frob_pos),len(frob_pos)), frob_pos, marker=".", s=0.8)
    # plt.scatter(positions_reduced["index"], frob_pos_reduced, marker=".", s=0.8, color=col)
    # plt.show()
