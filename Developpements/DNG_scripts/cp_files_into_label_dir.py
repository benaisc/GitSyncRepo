# coding: utf-8
# Script containing what is necessary to collect & manipulate CSV metadata extracted from EXIF of RAW images
# Author: Charles-Eric BENAIS-HUGOT, 28/03/2018

import sys, os
import pandas as pd
from shutil import copyfile


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


def distribute_files_into_camera_model_dir(groups, source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for model, group in groups:
        print("moving {} files into {} dir".format(len(group), model))
        os.makedirs(dest_dir_path+'/'+model)
        for filePathName in group['File name']:
            filePathNameArry = filePathName.split('/')
            dbName = filePathNameArry[-2]
            filename = filePathNameArry[-1]
            filename = os.path.splitext(filename)[0]+'.pgm'
            copyfile(source_dir_path+'/'+dbName+'/'+filename, dest_dir_path+'/'+model+'/'+filename)
			# in case you prefer to directly move the files instead of copying them
            #os.rename(source_dir_path+'/'+dbName+'/'+filename, dest_dir_path+'/'+model+'/'+filename)


def launch_():
    df = pd.DataFrame(columns=['File name', 'Camera model'])
    for metadata_csv in sys.argv[1:]:
        if(os.path.isfile(metadata_csv)):
            #print("___ {} ___".format(os.path.basename(metadata_csv)))
            dataframe = pd.read_csv(metadata_csv, index_col=False)
            df = pd.concat([df, dataframe[['File name', 'Camera model']]])


    df.to_csv('metadata_ALLTRAIN.csv', index=False, mode='w')
    #number_of_files_per_camera(df.groupby(by="Camera model"))
    #distribute_files_into_camera_model_dir(df.groupby(by="Camera model"),
    #                                      '/home/guru/STAGE/CODES/Developpements/DNG_scripts/DEVELOPPED_DATABASE',
    #                                      '/home/guru/STAGE/CODES/Developpements/DNG_scripts/TRAIN_DATA')


launch_() if len(sys.argv) > 1 else usage()
print('Success !')
