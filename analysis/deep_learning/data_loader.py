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


def __convert_into_ndarray(path_to_pic, index_no):
    assert os.path.exists(path_to_pic)

    img = np.array( Image.open(path_to_pic), 'f' )
    vector = __flatten_image(img)

    return (index_no, path_to_pic, vector)


def __make_data_mapping_dict(list_of_datasource):
    assert isinstance(list_of_datasource, list)
    path_source_mapper = {}
    list_of_array = []
    for data_source_info_tuple in list_of_datasource:
        assert isinstance(data_source_info_tuple, tuple)
        # save data array itself
        list_of_array.append(data_source_info_tuple[2])
        # save index id and its data content
        path_source_mapper[data_source_info_tuple[0]] = data_source_info_tuple[1]

    return path_source_mapper, list_of_array



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
    list_of_datasource = [
        __convert_into_ndarray(path_to_pic, index_no=index_no)
        for index_no, path_to_pic
        in enumerate(list_of_input_files)
    ]
    path_source_mapper, list_of_array = __make_data_mapping_dict(list_of_datasource)

    data_matrix = np.array(list_of_array)
    if is_convert==True:
        return path_source_mapper, data_matrix.astype(np.float32) /denominator
    else:
        return path_source_mapper, data_matrix.astype(np.float32)


def split_data_train_and_test(dataset, N):
    assert isinstance(N, int)
    assert isinstance(dataset, np.ndarray)
    assert len(dataset) > N

    train, test = np.split(dataset,   [N])
    N_test = test.shape[0]

    return {"train": train, "test": test, "N_test": N_test}


