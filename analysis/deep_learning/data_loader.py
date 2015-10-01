#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import glob
import os

from PIL import Image
import numpy as np


def make_path_pic_list(path_input_dir, suffix='*jpg'):
    return [
        path_to_pic
        for path_to_pic
        in glob.glob('{}/{}'.format(path_input_dir, suffix))
    ]


def __convert_into_ndarray(path_to_pic):
    assert os.path.exists(path_to_pic)

    img = np.array( Image.open(path_to_pic), 'f' )
    vector = __flatten_image(img)

    return vector




def __flatten_image(img):
    """
    takes in an (m, n) numpy array and flattens it
    into an array of shape (1, m * n)
    """
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, s)
    return img_wide[0]


def make_data_matrix(list_of_input_files, is_convert=True, denominator=255):
    """This method makes list of ndarray from picture data, which represents dataset

    :param list_of_input_files:
    :return:
    """
    assert isinstance(list_of_input_files, list)
    list_of_ndarray = [
        __convert_into_ndarray(path_to_pic)
        for path_to_pic
        in list_of_input_files
    ]

    data_matrix = np.array(list_of_ndarray)
    if is_convert==True:
        return data_matrix.astype(np.float32) /denominator
    else:
        return data_matrix.astype(np.float32)


def split_data_train_and_test(dataset, N):
    assert isinstance(N, int)
    assert isinstance(dataset, np.ndarray)
    assert len(dataset) > N

    train, test = np.split(dataset,   [N])
    N_test = test.shape[0]

    return {"train": train, "test": test, "N_test": N_test}


