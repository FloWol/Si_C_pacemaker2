import os
import gzip
import pandas as pd
import numpy as np
from ase import io
import matplotlib.pyplot as plt
#from compare_md_pace.compare_plots import  get_vals
"""
A really messy script where differences in energy forces and positions are calculated
and plotted

note that the differences are calculated between EACH step, which is the method implemented in ..
but different methods are used for the actual data selection
"""

#These 3 files show Si-C exchange
df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config1_rlx_at62_E14.25_b0_a0.pckl.gzip", compression="gzip")
#df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config2_rlx_at48_E15_b0_a0.pckl.gzip", compression="gzip")
#df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config9_rlx_at35_E14.75_b0_a0.pckl.gzip", compression="gzip")
#This below here has no exchange
#df = pd.read_pickle("/home/flo/pacemaker/data_grouped/Si_config8_rlx_at48_E3_b0_a0.pckl.gzip", compression="gzip")
#df = pd.read_pickle("/home/flo/pacemaker/Data_gzip/multi_trajectories_Si/displacements/config7/62/Si_config7_rlx_at62_E7.5_b0_a0.pckl.gzip", compression="gzip") #TODO check this

pace_path = "/home/flo/pacemaker/Data/multi_trajectories_Si/displacements/config9/35/Si_config9_rlx_at35_E14.75_b0_a0.traj"
pace_path = "/home/flo/pacemaker/Data/multi_trajectories_Si/displacements/config2/35/Si_config2_rlx_self_at35_E15.0_b0.0_a0.0.traj"
pace_md = io.Trajectory(pace_path, 'r')
def get_vals(images):
    data = {'energy': [],
            'forces': [],
            'ase_atoms': []}

    for i in range(len(images)):
        im = images[i]

        pe = im.get_potential_energy()


        data['energy'].append(pe)
        data['forces'].append(im.get_forces())
        data['ase_atoms'].append(im.copy())


    return pd.DataFrame(data)

df =  get_vals(pace_md)
# md_path = "/home/flo/pacemaker/Data/multi_trajectories_Si/displacements/config9/35/Si_config9_rlx_self_at35_E14.75_b0.0_a0.traj"
# df = get_vals(io.Trajectory(md_path, 'r'))

root_folder = "/home/flo/pacemaker/Data/"

energy_diff = df["energy"].diff()#np.zeros(shape=df["energy_corrected"].shape)
def plot_energy(energy_df):
    plt.plot(np.linspace(0,len(energy_df),len(energy_df)), energy_df)
    plt.show()
    plt.plot(np.linspace(0,len(energy_df),len(energy_df)), np.cumsum(energy_df))
    plt.show()
plot_energy(energy_diff)
# forces
forces_frob_norm = df['forces'].apply(lambda x : np.linalg.norm(x))
plt.plot(np.linspace(0,len(df["forces"]),len(df["forces"])), forces_frob_norm)
plt.title("Forces frob norm")
plt.show()
plt.plot(np.linspace(0,len(df["forces"]),len(df["forces"])), np.cumsum(forces_frob_norm))
plt.title("Forces frob norm cumsum")
plt.show()

plt.title("Forces max norm")
max_norm = df['forces'].diff()[1:].apply(lambda x : np.linalg.norm(x, ord=np.inf))
plt.plot(np.linspace(0,len(df["forces"])-1,len(df["forces"])-1), max_norm)
plt.show()
plt.title("Forces max norm cumsum")
plt.plot(np.linspace(0,len(df["forces"])-1,len(df["forces"])-1), np.cumsum(max_norm))
plt.show()
#
#
# #positions
# # Define a lambda function to calculate position differences
#
#
# # Apply the lambda function to the "ase_atoms"
diffs = [df['ase_atoms'][i].positions - df['ase_atoms'][i-1].positions
         for i in range(1, len(df))]
diffs_euklid = np.linalg.norm(diffs, axis=2)
euklid_euklid = np.linalg.norm(diffs_euklid, axis=1)
euklid_max = np.linalg.norm(diffs_euklid, axis=1, ord=np.inf)
frob = np.linalg.norm(diffs, ord="fro", axis=(1,2))

plt.plot(np.linspace(0,len(euklid_euklid),len(euklid_euklid)), euklid_euklid)
plt.title("positions 2x euclid norm")
plt.show()
plt.title("positions 2x euclid norm cumsum")
plt.plot(np.linspace(0,len(euklid_euklid),len(euklid_euklid)), np.cumsum(euklid_euklid))
plt.show()
plt.title("positions euclid to max norm")
plt.plot(np.linspace(0,len(euklid_max),len(euklid_max)), euklid_max)
plt.show()
plt.title("positions euclid to max norm cumsum")
plt.plot(np.linspace(0,len(euklid_max),len(euklid_max)), np.cumsum(euklid_max))
plt.show()

plt.title("diff positions frob norm")
plt.plot(np.linspace(0,len(frob),len(frob)), frob)
plt.show()
plt.title("diff positions frob norm cumsum")
plt.plot(np.linspace(0,len(frob),len(frob)), np.cumsum(frob))
plt.show()
#
#
positions = [df['ase_atoms'][i].positions
          for i in range(0, len(df))]
#
plt.title("positions frob norm")
frob_pos = np.linalg.norm(positions, ord="fro", axis=(1,2))
plt.plot(np.linspace(0,len(frob_pos),len(frob_pos)), frob_pos)
plt.show()
plt.title("positions frob norm cumsum")
plt.plot(np.linspace(0,len(frob_pos),len(frob_pos)), np.cumsum(frob_pos))
plt.show()

plt.title("positions eulid max norm")
pos_euklid = np.linalg.norm(positions, axis=2)
pos_euklid_max = np.linalg.norm(pos_euklid, axis=1, ord=np.inf)
plt.plot(np.linspace(0,len(pos_euklid_max),len(pos_euklid_max)), pos_euklid_max)
plt.show()
plt.title("positions eulid max norm cumsum")
plt.plot(np.linspace(0,len(pos_euklid_max),len(pos_euklid_max)), np.cumsum(pos_euklid_max))
plt.show()

plt.title("max amplitude x,y,z")
max_ampl = np.linalg.norm(positions, ord=np.inf, axis=1)
plt.plot(np.linspace(0,max_ampl.shape[0],max_ampl.shape[0]), max_ampl)
plt.legend(["X","Y","Z"])
plt.show()

#mean distance of atoms
plt.title("mean amplitude")
mean_ampl = np.mean(positions, axis=2)
mean_ampl = np.mean(mean_ampl, axis=1)
plt.plot(np.linspace(0,mean_ampl.shape[0],mean_ampl.shape[0]), mean_ampl)
plt.show()
#
# #mean distance per coordingate
plt.title("mean amplitude x,y,z")
mean_ampl = np.mean(positions, axis=1)
plt.plot(np.linspace(0,mean_ampl.shape[0],mean_ampl.shape[0]), mean_ampl)
plt.legend(["X","Y","Z"])
plt.show()

#max distance per atom
plt.title("max amplitude of atoms")
max_ampl = np.max(positions, axis=1)
max_ampl = np.max(max_ampl, axis=1)
plt.plot(np.linspace(0,max_ampl.shape[0],max_ampl.shape[0]), max_ampl)
plt.show()

#max distance per coordinate
plt.title("max amplitude of atoms x,y,z")
max_ampl = np.max(positions, axis=1)
plt.plot(np.linspace(0,max_ampl.shape[0],max_ampl.shape[0]), max_ampl)
plt.legend(["X","Y","Z"])
plt.show()

#do everything for every configuration
#parameters for setting the dataset

#do displacements in xyz coordinate
#do housekeeping
#put everything together