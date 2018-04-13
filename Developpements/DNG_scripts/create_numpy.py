import numpy as np
from pathlib import Path
from os.path import basename
import matplotlib.image as mpimg
import curses


def create_db(images_dir_path, numpy_filename):
    # Return a list of directories contained in images_dir_path
    labels_list = []
    dataset = [] # need (num_classes, num_exemple, h, w, c)
    for d in Path(images_dir_path).glob('*'):
        if not d.is_dir():
            continue;
        # Extract info about image dir path
        label = str(d).split('/')[-1]
        labels_list.append(label)
        print("Dir : {}".format(label))

        classDataSet = []
        for f in Path(d).glob('*.pgm'):
            #print("file: {}".format(basename(str(f))))
            img = mpimg.imread(f) # img.shape = (256, 256)
            img = np.reshape(img, newshape=(img.shape[0], img.shape[1], 1))
            #print("img.shape: {}".format(img.shape))
            classDataSet.append(img) # list numpy images

        dataset.append(classDataSet)
    return np.array(dataset), labels_list

def create_csv_labels(labelsList):
    file = open("train_db_labels.csv", "w")
    i=0
    for label in labelsList:
        #print("{} : {}".format(name, len(group)))
        file.write("{},{}\n".format(i, label))
        i += 1
    file.close()


numpy_filename = 'train_db.npy'
train_dir = '/home/guru/STAGE/CODES/Developpements/DNG_scripts/TRAIN_DATA'
data, labels = create_db(train_dir, numpy_filename)
np.save(numpy_filename, data)
create_csv_labels(labels)
