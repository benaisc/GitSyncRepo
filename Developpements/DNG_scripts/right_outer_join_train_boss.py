# coding: utf-8
# Script containing what is necessary to collect & manipulate CSV metadata extracted from EXIF of RAW images
# Author: Charles-Eric BENAIS-HUGOT, 28/03/2018

"""
This script is used to filter the intersection between two directories
"""
import sys, os
import pandas as pd
import numpy as np
from shutil import move


def usage():
    print("Usage: python {} path/to/data.csv".format(sys.argv[0]))
    print("i.e: python {} metadata_ALLTRAIN.csv metadata_BOSS.csv".format(sys.argv[0]))
    sys.exit()


def launch_():
    dfTRAIN = pd.read_csv(sys.argv[1], index_col=False)
    dfBOSS = pd.read_csv(sys.argv[2], index_col=False)

    camera_model_train = dfTRAIN['Camera model'].unique()
    camera_model_boss = dfBOSS['Camera model'].unique()
    npinter = np.intersect1d(camera_model_train, camera_model_boss)
    print("Intesect: {}".format(npinter))

    src = '/home/guru/STAGE/CODES/Developpements/DNG_scripts/TRAIN_DATA'
    dst = '/home/guru/STAGE/CODES/Developpements/DNG_scripts/NEW_DB'
    if not os.path.exists(dst):
        os.makedirs(dst)

    for model in npinter:
        dir = src + '/' + model
        if os.path.exists(dir):
            print("Moving {} to {}".format(dir, dst))
            move(dir, dst)

launch_() if len(sys.argv) > 1 else usage()
print('Success !')
