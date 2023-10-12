import numpy as np
import matplotlib.pyplot as plt
from ase import io
import pandas as pd
from pyace import *
import pickle
import os
import json


def calc_extraploration_grade(md_path):
    traj_md = io.Trajectory(md_path, 'r')

    calc = PyACECalculator("/home/flo/pacemaker/Data/potential_runs/Distance_10_potential/output_potential.yaml")
    calc.set_active_set("/home/flo/pacemaker/Data/potential_runs/Distance_10_potential/output_potential.asi")

    every_10th_img = traj_md[::10]

    #explorative_structures = []
    explorative_structures = io.Trajectory("/home/flo/pacemaker/Data/potential_runs/Distance_10_potential/extraploration_new.traj", 'a')

    # def calc_stuf(atoms):
    #     atoms.set_calculator(calc)
    #     atoms.get_potential_energy()
    #     gamma = calc.results["gamma"]
    #
    #     return calc.results
    #
    # np.apply_along_axis(every_10th_img)[["gamma"].max() > 5]


    for atoms in every_10th_img:
        atoms.set_calculator(calc)
        atoms.get_potential_energy()
        gamma = calc.results["gamma"]

        if gamma.max() > 5:
            #explorative_structures.append(atoms)
            explorative_structures.write(atoms)
            #do some calc and dumb

    return explorative_structures

root_folder = "/home/flo/pacemaker/Data/multi_Si"  # Change this to the root folder you want to start from
dump_folder = "/home/flo/pacemaker/Data/potential_runs/Distance_10_potential/dumps"
#writer = io.trajectory.TrajectoryWriter("/home/flo/pacemaker/Data/potential_runs/Distance_10_potential/extraploration.traj", 'w')

for root, _, files in os.walk(root_folder):
    for file in files:
        if file.endswith(".traj"):
            print("Processing file: " + str(file))
            traj_file_path = os.path.join(root, file)
            dump_file_path = os.path.join(dump_folder, file[:-5] + ".dump")

            calc_extraploration_grade(traj_file_path)

            # Store the output in the corresponding .dump file
            #if extrastruct != []:
            #    for img in extrastruct:
            #       writer.write(img)

print("done")
