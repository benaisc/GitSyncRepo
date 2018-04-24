import numpy as np


def load_dataset():
    # [num_classes, num_samples, im_height, im_width, im_channels]
    x = np.load("datasets/lirmm_db.npy")
    print("x.shape: {}".format(x.shape))
    #print("Total images: {}".format(count_images(x))

    x_val, x_test, x_train = x[:3], x[3:25], x[25:]

    return x_train, x_test, x_val

def count_images(x_var):
    total=0
    for i in range(x_var.shape[0]):
        #print("c{} : {}".format(i, len(x_var[i])))
        total += len(x_var[i])
    return total

def normalize_images(x_var):
    print("for i in range({})".format(x_var.shape[0]))
    for i in range(x_var.shape[0]):
        print("for j in range({})".format(len(x_var[i])))
        for j in range(len(x_var[i])):
            x_var[i][j] = x_var[i][j].astype('float64')
            #x_var[i][j] = (x_var[i][j] - x_var[i][j].min()) / (x_var[i][j].max() - x_var[i][j].min())
            x_var[i][j] /= 255.0
    return x_var

x_train, x_test, x_val = load_dataset()
print("x_train.shape: {}\nx_test.shape: {}\nx_val.shape: {}".format(x_train.shape, x_test.shape, x_val.shape))
print("x_train.shape[0]: {} * x_train.shape[1]: {}".format(x_train.shape[0], x_train.shape[1]))
#print("x_train: {}".format(count_images(x_train)))
#print("x_test: {}".format(count_images(x_test)))
#print("x_val: {}".format(count_images(x_val)))
