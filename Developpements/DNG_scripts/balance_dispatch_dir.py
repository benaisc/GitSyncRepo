from pathlib import Path
from shutil import copy
import os
from random import shuffle

"""
This script is used to random select files over all directories contained in path
First, we select all directories containing more than 500 files
Then, we shuffle the randomly selected 590 files &n distribute them into dest_dir
"""
def select_n_distribute(dir_path, dest_dir):
    # Return a list of directories contained in images_dir_path
    dir_list = [str(d) for d in Path(dir_path).glob('*') if d.is_dir()]
    print("There is {} directories :".format(len(dir_list)))

    for d in Path(dir_path).glob('*'):
        if not d.is_dir():
            continue;

        label = str(d).split('/')[-1]
        file_list = [str(f) for f in Path(d).glob('*.pgm')]
        if len(file_list) > 500:
            print("{} : {}".format(label, len(file_list)))
            os.makedirs(dest_dir+'/'+label)
            print("Shuffling...")
            shuffle(file_list)
            print("Copying...")
            for i in range(590):
                copy(file_list[i], str(dest_dir)+'/'+label)


train_dir = '/home/guru/STAGE/CODES/Developpements/DNG_scripts/TRAIN_DATA'
dest_dir = '/home/guru/STAGE/CODES/Developpements/DNG_scripts/LIRMMv0'

select_n_distribute(train_dir, dest_dir)
