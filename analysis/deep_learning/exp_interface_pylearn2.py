#! -*- coding: utf-8 -*-
from core_pylearn2 import make_dataset_pylearn2
from core_pylearn2 import train_model_pylearn2
from core_pylearn2 import data_loader
from pylearn2.testing import skip

import os

__author__ = 'kensuke-mi'


def make_girls_face_dbm_model():
    """make dataset for pylearn2 from girls' face gray scaled pictures
    :return:
    """
    path_index_path = '../../extracted/miss_collection/gray'
    input_files_list = data_loader.make_path_pic_list(path_input_dir=path_index_path)

    PATH_TO_DATA_DIR = 'pylearn2_intermediate_files'
    PROJECT_NAME = 'girls_face_dmb'
    make_dataset_pylearn2.main(input_files_list, PATH_TO_DATA_DIR, PROJECT_NAME)

    PATH_TO_PYLEARN2_MODES_DIR = os.path.abspath(os.path.join('core_pylearn2', 'model_pylearn2'))
    PATH_TO_INPUT_DIR = os.path.abspath(os.path.join(PATH_TO_DATA_DIR, PROJECT_NAME))

    skip.skip_if_no_data()
    train_model_pylearn2.train_dbm_model(PATH_TO_PYLEARN2_MODES_DIR, PATH_TO_INPUT_DIR, PROJECT_NAME)


if __name__ == '__main__':
    make_girls_face_dbm_model()