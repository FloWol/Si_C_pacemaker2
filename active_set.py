import numpy as np
import matplotlib.pyplot as plt
from ase import io
import pandas as pd
from pyace import *



pace_path="/home/flo/pacemaker/Data/multi_Si/displacements/config4/34/Si_config4_rlx_self_1st_at34_E15.25_b0.0_a0.0.traj"
md_path="/home/flo/pacemaker/Data/multi_Si/displacements/config4/34/Si_config4_rlx_at34_E15.25_b0_a0.traj"


traj_md = io.Trajectory(md_path, 'r')
pace_md = io.Trajectory(pace_path, 'r')


atoms = io.read(md_path)
calc = PyACECalculator("output_potential.yaml")
calc.set_active_set("output_potential.asi")

# set calculator to ASE atoms
atoms.set_calculator(calc)

# trigger calculation
atoms.get_potential_energy()

#per-atom extrapolation grades are stored in
calc.results["gamma"]