import numpy as np
import matplotlib.pyplot as plt
from ase import io
import pandas as pd

#atom 49 config 1 E18 no exchange
md_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config1/atom49/Si_config1_rlx_at49_E18_b0_a0.traj"
pace_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config1/atom49/Si_config1_rlx_self_at49_E18.0_b0.0_a0.traj"

#Atom 62 config 1 E 14.25 exchange
md_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config1/atom62/Si_config1_rlx_at62_E14.25_b0_a0.traj"
pace_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config1/atom62/Si_config1_rlx_self_at62_E14.25_b0.0_a0.traj"

#Atom 48 config 2 E 15 exchange
md_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config2/48/Si_config2_rlx_at48_E15_b0_a0.traj"
pace_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config2/48/Si_config2_rlx_self_at48_E15.0_b0.0_a0.traj"

# md_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config9/35/Si_config9_rlx_self_at35_E14.75_b0.0_a0.traj"
# pace_path = "/home/flo/pacemaker/Data2/multi_trajectories_Si/displacements/config9/35/Si_config9_rlx_at35_E14.75_b0_a0.traj"
#
# md_path = "/home/flo/pacemaker/Data2/single_trajectories_Si/14eV/alpha65/gra66_triSi_rlx_at29_E14.0_a-30_b65.0.traj"
# pace_path = "/home/flo/pacemaker/Data2/single_trajectories_Si/14eV/alpha65/gra66_triSi_rlx_self_at29_E14.0_a30.0_b65.0.traj"


md_path = "/home/flo/pacemaker/Data/multi_Si/displacements/config5/49/Si_config5_rlx_at49_E17.5_b0_a0.traj"
pace_path = "/home/flo/pacemaker/Data/multi_Si/displacements/config5/49/Si_config5_rlx_self_at49_E17.5_b0.0_a0.0.traj"

traj_md = io.Trajectory(md_path, 'r')
pace_md = io.Trajectory(pace_path, 'r')

def get_vals(images):
    data = {'energy': [],
            'forces': []}

    for i in range(len(images)):
        im = images[i]

        pe = im.get_potential_energy()


        data['energy'].append(pe)
        data['forces'].append(im.get_forces())


    return pd.DataFrame(data)

md_data =  get_vals(traj_md)
pace_data = get_vals(pace_md)

plt.scatter(md_data.index.values, md_data["forces"].apply(lambda x : np.linalg.norm(x)), marker=".", s=0.8, label="MD")
plt.scatter(pace_data.index.values, pace_data["forces"].apply(lambda x : np.linalg.norm(x)), marker=".", s=0.8, label="ML")
plt.legend()
plt.show()

print(md_data["forces"].apply(lambda x : np.linalg.norm(x))-pace_data["forces"].apply(lambda x : np.linalg.norm(x)))