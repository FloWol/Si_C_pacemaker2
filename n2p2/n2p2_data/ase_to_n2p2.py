#!/usr/bin/env python3
import numpy as np
from ase import Atoms
from ase.calculators.singlepoint import SinglePointCalculator
from ase import io
from ase import units

"""
Little script from the ase package a little adjusted to convert ase.traj to n2p2.data files
"""

def _write_n2p2(fid, atoms, comment='', with_charges=False, with_energy_and_forces='auto'):
    # float_form = "{: 13.8f}" # looks nicer but, results can be very sensitive
    float_form = "{: 1.16E}"  # {: 1.16E} is what N2P2 uses in outout.data so we should match them
    lattice_format = "lattice  %s  %s  %s\n" % tuple(3 * [float_form])
    atom_format = "atom %s %s %s   {} %s %s %s %s %s\n" % tuple(8 * [float_form])
    unused_column = [0.0]

    fid.write('begin\n')
    if comment != '':
        fid.write('comment %s\n' % comment)

    for i in range(3):
        fid.write(lattice_format.format(*atoms.cell[i]))

    # deciding what to do about energies and forces
    fillzeros = True
    if with_energy_and_forces == True:
        fillzeros = False

    if type(with_energy_and_forces) == str:
        if with_energy_and_forces.lower() == 'auto':
            # if hasattr(atoms, 'calc'):
            if atoms._calc is not None:
                fillzeros = False
            else:
                fillzeros = True

    if fillzeros:
        energy = 0.0
        forces = np.zeros((len(atoms), 3))
    else:
        energy = atoms.get_potential_energy()
        forces = atoms.get_forces()

    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()
    unuseds = unused_column * len(atoms)

    if with_charges:
        charges = atoms.get_charges()
    else:
        charges = np.zeros(len(atoms))

    for data in zip(positions[:, 0], positions[:, 1], positions[:, 2],
                    symbols, charges, unuseds,
                    forces[:, 0], forces[:, 1], forces[:, 2]):
        fid.write(atom_format.format(*data))
    if not fillzeros:
        fid.write(('energy %s\n' % float_form).format(energy))
    fid.write('end\n')


def write_n2p2(
        filename,  # ='input.data',
        images,
        comment='',
        with_charges=False,
        with_energy_and_forces='auto'):
    # filename is typically 'input.data'

    fid = open(filename, 'w')
    if type(images) is Atoms:
        atoms = images
        _write_n2p2(fid, atoms, comment, with_charges, with_energy_and_forces)
    else:
        for atoms in images:
            _write_n2p2(fid, atoms, comment, with_charges, with_energy_and_forces)
    fid.close()

if __name__ == '__main__':
    source='/home/flo/pacemaker/Data/multi_trajectories_Si/displacements/config1/atom62/Si_config1_rlx_at62_E14.25_b0_a0.traj'
    traj = io.Trajectory(source, 'r')
    write_n2p2("testing.data",traj, comment=source,with_energy_and_forces=True)
    print("done")

