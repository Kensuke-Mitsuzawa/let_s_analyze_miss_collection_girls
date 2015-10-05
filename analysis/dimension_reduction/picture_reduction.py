#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import glob
from modules.data_loader_picture import PictureDataLoader

PATH_TO_PICS_DIR = '../../extracted/miss_collection/gray'
PATH_TO_SAVE_PICKLE = './data_directory/picture_matrix_obj.pickle'

def make_path_pic_list(path_input_dir, suffix='*jpg'):
    return [
        path_to_pic
        for path_to_pic
        in glob.glob('{}/{}'.format(path_input_dir, suffix))
    ]


def prepare_picture_data_matrix(path_input_dir, path_to_save_pickle):

    list_path_to_pic_file = make_path_pic_list(path_input_dir)
    pic_data_loader_obj = PictureDataLoader(list_path_to_images=list_path_to_pic_file)
    path_index_mapper, picture_data_matrix = pic_data_loader_obj.make_data_matrix()
    pic_data_loader_obj.save_into_pickle(path_pickle_file=path_to_save_pickle)


if __name__ == '__main__':
    prepare_picture_data_matrix(PATH_TO_PICS_DIR, PATH_TO_SAVE_PICKLE)


