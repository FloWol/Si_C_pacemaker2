import pandas as pd
import tensorflow as tf
def main():
    df = pd.read_pickle("/home/flo/pacemaker/Data/single_trajectories_Si/14.5eV/alpha30/gra66_triSi_rlx_at29_E14.5_a0_b30.0.pckl.gzip", compression="gzip")
    print(df)
    print(tf.config.list_physical_devices('GPU'))
    return 0


if __name__ == '__main__':
    main()



#Researchredundancy
# check out https://pacemaker.readthedocs.io/en/latest/pacemaker/quickstart/
# look further into the ASE_to_Pacemaker script
# look into the data
# check this out https://wiki.fysik.dtu.dk/ase/ase/atoms.html
# check out https://github.com/ICAMS/python-ace/tree/master/examples for examples
#look into active learning

#Questions
# what are thes cutoffs?   cutoffs: carbon 0.64(comp), 1.14(filt), 1.14(core), lmax=2 from the data
#silicon silicon  cutoffs: 1.06(comp), 1.86(filt), 2.06(core), lmax=2 reference energy -80847.940449
# from pacemaker  ## only the structures with energy up to E_min + DEup will be selected

#Todo's merge datasets? -> write scripts
#maybe make a proper class/programm/wrapper for data collection and redundancy
#Todo figure out redundancy -> look into ase?
#Todo remote interpreter would be ideal
#Write a script to test the perfromance/potential, using ase and copying the structures


#Morgen PACEMAKER paper und examples durchgehen
# VelocityVerlet(atoms, 0.3*units.fs) 1800 steps
#Data//multi_trajectories_Si/displacements/test/Si_config1_rlx_at48_E17.5_b0_a0.traj could not be converted

#how to get energy radius curves, volume and phonons



#read through ACE to see what b basis etc is


#Tomorrow: Set up the dataset and start implementing the data reduction
