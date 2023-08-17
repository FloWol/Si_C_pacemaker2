import os
from ase_to_n2p2 import write_n2p2
from ase import io

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".traj"):
                print("processing_file: " + str(file))
                full_path = os.path.join(root, file)
                input_filename = os.path.splitext(file)[0] + '.data'
                try:
                    traj = io.Trajectory(full_path, 'r')
                    write_n2p2(input_filename,traj, comment=str(file),with_energy_and_forces=True)
                except Exception as e:
                    print(f"Error processing files {full_path} and {file}: {e}")


# Replace 'your_directory_path' with the actual path of the directory you want to scan
print("starting ...")
process_directory('/home/flo/pacemaker/Data/multi_Si')
print("done")
