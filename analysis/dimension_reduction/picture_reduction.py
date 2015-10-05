#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import glob
from modules.data_loader_picture import PictureDataLoader
from modules.space_converter_with_deep_learning import SpaceConverterDeepFeature
import os
import numpy

PATH_TO_PICS_DIR = '../../extracted/miss_collection/gray'
PATH_TO_SAVE_PICKLE = './data_directory/picture_matrix_obj.pickle'


def make_path_pic_list(path_input_dir, suffix='*jpg'):
    return [
        path_to_pic
        for path_to_pic
        in glob.glob('{}/{}'.format(path_input_dir, suffix))
    ]


def prepare_picture_data_matrix(path_input_dir, path_to_save_pickle):
    assert os.path.exists(path_input_dir)
    assert os.path.exists(os.path.dirname(path_to_save_pickle))

    list_path_to_pic_file = make_path_pic_list(path_input_dir)
    pic_data_loader_obj = PictureDataLoader(list_path_to_images=list_path_to_pic_file)
    path_index_mapper, picture_data_matrix = pic_data_loader_obj.make_data_matrix()
    pic_data_loader_obj.save_into_pickle(path_pickle_file=path_to_save_pickle)


def prepare_picture_matrix_with_trained_features(path_to_trained_model_pickle, vector_numbers_index):
    #vector_numbers_index = [0, 10, 100]
    assert os.path.exists(path_to_trained_model_pickle)
    assert isinstance(vector_numbers_index, list)

    space_convert_obj = SpaceConverterDeepFeature(path_to_trained_model_pickle=path_to_trained_model_pickle)
    selected_vectors = space_convert_obj.select_feature_vectors(vector_index_numbers=vector_numbers_index)
    converted_matrix = space_convert_obj.space_convert(feature_vectors=selected_vectors)
    assert isinstance(converted_matrix, numpy.ndarray)

if __name__ == '__main__':
    prepare_picture_data_matrix(PATH_TO_PICS_DIR, PATH_TO_SAVE_PICKLE)
    path_to_trained_model_pickle = '../test/relu_2layer_simple_test.pickle'


