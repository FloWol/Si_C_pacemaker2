import pandas as pd
from ase import Atoms
"""
This is an example from the pacemaker documentation.
The data it creates can be used to compare it with your data
to check if the formating etc. is correct.
"""
# Collect raw data for the first structure
# Positions
pos1 = [[2.04748516, 2.04748516, 0.        ],
       [0.        , 0.        , 0.        ],
       [2.04748516, 0.        , 1.44281847],
       [0.        , 2.04748516, 1.44475745]]
# Matrix of lattice vectors
lattice1 = [[4.09497 , 0.      , 0.      ],
       [0.      , 4.09497 , 0.      ],
       [0.      , 0.      , 2.887576]]
# Atomic symbols
symbls1 = ['Al', 'Al', 'Ni', 'Ni']
# energy
e1 = -21.07723361
# Forces
f1 = [[0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0],
     [0.0, 0.0, 0.00725587],
     [0.0, 0.0, -0.00725587]]
# create ASE atoms
at1 = Atoms(symbols=symbls1, positions=pos1, cell=lattice1, pbc=True)

#Collect raw data for the second structure
pos2  = [[0., 0., 0.]]
lattice2 = [[0.      , 1.781758, 1.781758],
           [1.781758, 0.      , 1.781758],
           [1.781758, 1.781758, 0.      ]]
symbls2 = ['Ni']
e2 = -5.45708644
f2 = [[0.0, 0.0, 0.0]]
at2 = Atoms(symbols=symbls2, positions=pos2, cell=lattice2, pbc=True)

# set reference energy to 0
reference_energy = 0
# collect all the data into a dictionary
data = {'energy': [e1, e2],
        'forces': [f1, f2],
        'ase_atoms': [at1, at2],
        'energy_corrected': [e1 - reference_energy, e2 - reference_energy]}
# create a DataFrame
df = pd.DataFrame(data)
# and save it
df.to_pickle('my_data.pckl.gzip', compression='gzip', protocol=4)