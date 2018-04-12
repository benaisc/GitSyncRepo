# coding: utf-8
# Script containing what is necessary to collect & manipulate CSV metadata extracted from EXIF of RAW images
# Author: Charles-Eric BENAIS-HUGOT, 28/03/2018

import sys, os
import pandas as pd


def usage():
    print("Usage: python {} path/to/data.csv".format(sys.argv[0]))
    print("i.e: python {} $(find . -type f -name \"metadata_*.csv\")".format(sys.argv[0]))
    sys.exit()


def number_of_files_per_camera(groups):
    file = open("number_of_files_per_camera.csv", "w")
    file.write("Camera model, n\n")
    for name, group in sorted(groups, key=lambda x: len(x[1]), reverse=True):
        #print("{} : {}".format(name, len(group)))
        file.write("{},{}\n".format(name, len(group)))

    file.close()


def distribute_files_into_camera_model_dir(groups, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for model, group in groups:
        print("moving {} files into {} dir".format(len(group), model))
        os.makedirs(dest_dir_path+'/'+model)
        for filename in group['File name']:
            os.rename(filename, dest_dir_path+'/'+model+'/'+os.path.basename(filename))
            

def launch_():
    df = pd.DataFrame(columns=['File name', 'Camera model'])
    for metadata_csv in sys.argv[1:]:
        if(os.path.isfile(metadata_csv)):
            #print("___ {} ___".format(os.path.basename(metadata_csv)))
            dataframe = pd.read_csv(metadata_csv, index_col=False)
            df = pd.concat([df, dataframe[['File name', 'Camera model']]])

    #number_of_files_per_camera(df.groupby(by="Camera model"))
    distribute_files_into_camera_model_dir(df.groupby(by="Camera model"),
                                          '/home/guru/STAGE/CODES/Developpements/DNG_scripts/TRAIN_DATA')


launch_() if len(sys.argv) > 1 else usage()
print('Success !')