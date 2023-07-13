# From Michael J Waters (Matrix chat, 15.3.2023)

import os, sys

from ase import io 
import pandas as pd

from ase.data import chemical_symbols

def make_input_data(images, data_file, id_list=None):
    ref_energies = {}
    for element in chemical_symbols:
        
        ref_file = '%s_reference.traj'%element
        ref_energies[element]=0.0
        if os.path.isfile(ref_file):
            isolated = io.read()
            ref_energies[element] =  isolated.get_potential_energy()
        
    def reference_energy(atoms, ref_energies=ref_energies):
        E = 0
        for atom in atoms:
            E += ref_energies[atom.symbol]
        return E

    #data = {'energy': [e1, e2], 
    #        'forces': [f1, f2], 
    #        'ase_atoms': [at1, at2], 
    #        'energy_corrected': [e1 - reference_energy, e2 - reference_energy]}

    

    data = {'energy': [], 
            'forces': [], 
            'ase_atoms': [], 
            'energy_corrected': []}
    if id_list is not None:
        data['id']=[]

    for i in range(len(images)):
        im = images[i]
        
        pe = im.get_potential_energy()
        pe_corrected = pe - reference_energy(im)
        
        data['energy'].append(pe)
        data['forces'].append(im.get_forces())
        data['ase_atoms'].append(im.copy())
        data['energy_corrected'].append(pe_corrected)

        if id_list is not None:
            data['id'].append(id_list[i])

    #print(data)

    # create a DataFrame
    df = pd.DataFrame(data)
    # and save it 
    df.to_pickle(data_file, compression='gzip', protocol=4)


file = sys.argv[1]
name = os.path.splitext(file)[0]

traj = io.Trajectory(file,'r')
make_input_data(traj, name + '.pckl.gzip')
print("succes!")
