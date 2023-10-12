#!/usr/bin/env python
import sys, os, math
import numpy as np
#from gpaw.utilities.bulk2 import GPAWRunner
from ase import io
from ase import Atom
from ase.units import Bohr

from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units

from ase.io import Trajectory, read
from pyace import PyACECalculator

filename = str(sys.argv[1])
name = os.path.splitext(filename)[0]

atoms = io.read(filename)
atoms2 = atoms.copy()

at = int(sys.argv[2])
# E = float(sys.argv[3]) # Intial kinetic energy in eV
# a = float(sys.argv[4]) # Spherical angle beta
alpha = 0  # Spherical angle alpha

betaval = [0]
tdvalues = [17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5]

flog = open("displacement_log.txt", 'w')


def checkejected(a=atoms):  # store a reference to atoms in the definition.
    if atoms[at].position[2] > 14.1:

        flog.write(str(E))
        flog.write('\n')
        return False
    else:
        return True


for beta in betaval:

    for E in tdvalues:

        atoms = atoms2.copy()

        outname = name + "_at" + str(at) + "_E" + str(E) + "_b" + str(beta) + "_a" + str(alpha)
        # set gpaw
        myk = 3
        calc = PyACECalculator("output_potential.yaml")
        calc.set_active_set("output_potential.asi")

        atoms.set_calculator(calc)

        MaxwellBoltzmannDistribution(atoms, 1 * units.kB)

        dyn = VelocityVerlet(atoms, 0.3 * units.fs)
        traj = Trajectory(outname + '.traj', 'w', atoms)
        dyn.attach(traj.write, interval=1)
        dyn.run(1)
        # attach the observer
        dyn.attach(checkejected, interval=1)

        v = (2 * float(E) / atoms[at].mass) ** 0.5

        vx = v * math.sin(math.pi * beta / 180) * math.cos(math.pi * alpha / 180)
        vy = v * math.sin(math.pi * beta / 180) * math.sin(math.pi * alpha / 180)
        vz = v * math.cos(math.pi * beta / 180)

        atoms[at].momentum[0] = atoms[at].mass * vx
        atoms[at].momentum[1] = atoms[at].mass * vy
        atoms[at].momentum[2] = atoms[at].mass * vz

        while checkejected(atoms) == True:
            for step in range(400):
                dyn.run(1)
            break

        traj.close()
        if atoms[at].position[2] > 14.1:
            break