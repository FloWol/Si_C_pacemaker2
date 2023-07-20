import numpy as np
import pandas as pd

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
        differences = data['forces'].diff().apply(lambda x: np.linalg.norm(x))

    if(metric == "distance"):
        diff_pos = [data['ase_atoms'][i].positions - data['ase_atoms'][i - 1].positions
                 for i in range(1, len(data))]
        differences = np.linalg.norm(diff_pos, ord="fro", axis=(1, 2))

    #check if they are above the threshold
    indices = np.where(differences < threshold)[0]

    #return new dataset
    return data.iloc[indices]


df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config9_rlx_at35_E14.75_b0_a0.pckl.gzip", compression="gzip")
data_filterd=reduce_redundancy(df, "energy_corrected", 0.01)
reducion_degree = data_filterd.shape[0]/df.shape[0]
print("energy_corrected: Data was reduced by {:.2f}% ".format(reducion_degree*100))
#0.01 for energy values filters around 50% of the data
#test some more
#for frob norm (at least in case of exchange) try 0.001-0.005
data_filterd=reduce_redundancy(df, "distance", 0.02)
reducion_degree = data_filterd.shape[0]/df.shape[0]
print("Distance: Data was reduced by {:.2f}% ".format(reducion_degree*100))

#for forces 0.3?
data_filterd=reduce_redundancy(df, "forces", 0.3)
reducion_degree = data_filterd.shape[0]/df.shape[0]
print("Forces: Data was reduced by {:.2f}% ".format(reducion_degree*100))
