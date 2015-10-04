#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
import face_extract
import glob
import os


def make_save_paths(PATH_INPUT_DIR, PATH_SAVE_DIR):
    input_output_save_dict = {}
    for path, dirs, files in os.walk(PATH_INPUT_DIR):
        assert isinstance(dirs, list)
        assert isinstance(files, list)
        for dir_name in dirs:
            for f_lists in glob.glob(os.path.join(path, dir_name, "*jpg")):
                path_to_file = f_lists
                path_to_save = os.path.join(PATH_SAVE_DIR, os.path.split(path_to_file)[-1])
                input_output_save_dict[path_to_file] = path_to_save

    return input_output_save_dict


def girls_face_process():
    PATH_INPUT_DIR = '../../extracted/miss_collection_old/old_pics'
    PATH_SAVE_DIR = '../../extracted/miss_collection/face'

    assert os.path.exists(PATH_INPUT_DIR)
    assert os.path.exists(os.path.dirname(PATH_SAVE_DIR))
    if os.path.exists(PATH_SAVE_DIR)==False: os.mkdir(PATH_SAVE_DIR)
    input_output_save_dict = make_save_paths(PATH_INPUT_DIR, PATH_SAVE_DIR)


    for index, path_input, path_save in enumerate(input_output_save_dict.items()):
        face_extract.main_procedure(imagefile_name=path_input, path_to_save=path_save)


if __name__ == '__main__':
    #example_usage()
    girls_face_process()