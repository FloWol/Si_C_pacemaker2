import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
This version is like reduce_data, but here we we compare it to the last structure taken and not 
the immediate difference between two rows
"""

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


    # Iterate over the DataFrame rows using itertuples
    for row in df.itertuples(index=True):
        current_value = row[index_dict[metric]]
        difference = diff_function(last_taken, current_value)
        #df.loc[row[0], 'Difference'] = difference #not good FIXME

        # Check if the difference exceeds the threshold
        if abs(difference) > threshold:
            df.loc[row[0], 'Difference'] = difference  #not good FIXME
            # Update the last taken value
            last_taken = current_value
    if(full_return):
        return df
    else:
        return df[np.abs(df["Difference"]) > threshold].iloc[:, :4].reset_index(drop=True)



def plot_df(energy_df):
    plt.scatter(np.linspace(0,len(energy_df),len(energy_df)), energy_df, marker=".", s=0.8)
    plt.show()

if __name__ == '__main__':
    df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config9_rlx_at35_E14.75_b0_a0.pckl.gzip", compression="gzip")
    data_filterd=reduce_redundancy(df, "energy_corrected", 0.1)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("energy_corrected: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    plot_df(df["energy_corrected"])
    plot_df(data_filterd["energy_corrected"])

    #for forces 0.3?
    norm=np.inf
    data_filterd=reduce_redundancy(df, "forces", 0.3,norm=norm)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("Forces: Data was reduced to {:.2f}% ".format(reducion_degree*100))

    forces_frob_norm = df['forces'].apply(lambda x : np.linalg.norm(x, ord=norm))
    forces_frob_norm_reduced = data_filterd["forces"].apply(lambda x: np.linalg.norm(x, ord=norm))
    plot_df(forces_frob_norm)
    plot_df(forces_frob_norm_reduced)

    norm=np.inf
    data_filterd=reduce_redundancy(df, "distance", 0.3, norm=norm)
    reducion_degree = data_filterd.shape[0]/df.shape[0]
    print("Distance: Data was reduced to {:.2f}% ".format(reducion_degree*100))
    positions = [df['ase_atoms'][i].positions
              for i in range(0, len(df))]
    frob_pos = np.linalg.norm(positions, ord=norm, axis=(1,2))

    positions_reduced = [data_filterd['ase_atoms'][i].positions
              for i in range(0, len(data_filterd))]
    frob_pos_reduced = np.linalg.norm(positions_reduced, ord=norm, axis=(1,2))
    plot_df(frob_pos)
    plot_df(frob_pos_reduced)
