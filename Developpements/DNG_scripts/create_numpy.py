import numpy as np
from pathlib import Path
from os.path import basename
import matplotlib.image as mpimg
import curses

"""
This script read all files recursively in given directory, create a class of
each dir, and put the images (normalized numpy arrays) in a npy binary format
in the form: (num_classes, num_exemple, h, w, c)
"""

def create_db(images_dir_path):
    # Return a list of directories contained in images_dir_path
    labels_list = []
    dataset = [] # need (num_classes, num_exemple, h, w, c)
    file = open("db_labels.csv", "w")
    file.write("label_id, label, number_images")
    i=0
    for d in Path(images_dir_path).glob('*'):
        if not d.is_dir():
            continue;
        # Extract info about image dir path
        label = str(d).split('/')[-1]
        labels_list.append(label)
        print("Dir : {}".format(label))

        classDataSet = []
        for f in Path(d).glob('*.pgm'):
            img = mpimg.imread(f) # img.shape = (256, 256)
            img = img.astype(np.float)
            img /= 255.0
            img = np.reshape(img, newshape=(img.shape[0], img.shape[1], 1))
            classDataSet.append(img) # list numpy images

        file.write("{},{},{}\n".format(i, label, len(classDataSet)))
        i += 1
        dataset.append(classDataSet)

    return np.array(dataset), labels_list

def create_csv_labels(labelsList):
    file = open("lirmm_db_labels.csv", "w")
    i=0
    for label in labelsList:
        #print("{} : {}".format(name, len(group)))
        file.write("{},{}\n".format(i, label))
        i += 1
    file.close()

numpy_filename = 'lirmm_db.npy'
train_dir = '/home/guru/STAGE/CODES/Developpements/DNG_scripts/TRAIN_DATA'
data, labels = create_db(train_dir)
np.save(numpy_filename, data)
create_csv_labels(labels)
