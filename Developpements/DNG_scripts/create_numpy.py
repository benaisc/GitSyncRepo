import numpy as np
from pathlib import Path
from os.path import basename
import matplotlib.image as mpimg
import curses


def create_db(images_dir_path):
    # Return a list of directories contained in images_dir_path
    csvInfo = []
    dataset = [] # need (num_classes, num_exemple, h, w, c)
    file = open("lirmm_128_labels.csv", "w")
    file.write("label_id, label, number_images\n")
    i=0
    for d in Path(images_dir_path).glob('*'):
        if not d.is_dir():
            continue;
        # Extract info about image dir path
        label = str(d).split('/')[-1]
        print("Dir : {}".format(label))

        classDataSet = []
        for f in Path(d).glob('*.pgm'):
            img = mpimg.imread(f) # img.shape = (256, 256)
            img = img.astype(np.float)
            img /= 255.0
            img = np.reshape(img, newshape=(img.shape[0], img.shape[1], 1))
            classDataSet.append(img) # list numpy images

        csvInfo.append([i, label, len(classDataSet)])
        dataset.append(classDataSet)
        i += 1

    dataset.sort(key=len)
    csvInfo.sort(key=lambda item: item[2])
    for i in range(len(csvInfo)):
        file.write("{},{},{}\n".format(csvInfo[i][0], csvInfo[i][1], csvInfo[i][2]))

    return np.array(dataset)



train_dir = '/media/icar/269f599f-6a72-48fd-b97c-941595d7b39f/Charles/128/128_TRAIN_DATA'
if not Path(train_dir).is_dir():
    print('Error')
    exit()
data = create_db(train_dir)
np.save('lirmm_128.npy', data)
