import numpy as np
import skimage.io as io
from pathlib import Path


def img_encode_tostr(img):
    img_shape = img.shape
    img_str = img.tostring()
    return img_str, img_shape

def img_decode_fromstr(img_str, img_shape):
    reconstructed_img_1d = np.fromstring(img_str, dtype=np.uint8)
    return reconstructed_img_1d.reshape(img_shape)

images_dir_path = '/home/guru/STAGE/CODES/Developpements/DNG_scripts/TRAIN_DATA/'

pathlist = Path(images_dir_path).glob('**/*.pgm')
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    #print(path_in_str)

    img = io.imread(path_in_str)

    str_img, img_shape = img_encode_tostr(img)

    reconstructed_img = img_decode_fromstr(str_img, img_shape)

    print(np.allclose(img, reconstructed_img))