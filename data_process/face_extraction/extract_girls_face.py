#! -*- coding: utf-8 -*-
import face_extract
import glob
import os
import re

__author__ = 'kensuke-mi'


def make_save_paths(PATH_INPUT_DIR, PATH_SAVE_DIR):
    input_output_save_dict = {}
    for path, dirs, files in os.walk(PATH_INPUT_DIR):
        assert isinstance(dirs, list)
        assert isinstance(files, list)
        for dir_name in dirs:
            for f_lists in glob.glob(os.path.join(path, dir_name, "*jpg")):
                path_to_file = os.path.abspath(f_lists)
                file_name = os.path.split(path_to_file)[-1]
                if re.findall(ur'.*_\d', file_name)==[]:
                    f_name, ext = os.path.splitext(file_name)
                    new_file_name = '{}_main{}'.format(f_name, ext)
                else:
                    new_file_name = file_name

                path_to_save = os.path.join(PATH_SAVE_DIR, new_file_name)
                input_output_save_dict[path_to_file] = os.path.abspath(path_to_save)

    return input_output_save_dict


def girls_face_process():
    PATH_INPUT_DIR = '../../extracted/miss_collection/original_pic'
    PATH_SAVE_DIR = '../../extracted/miss_collection/face'
    PATH_TO_RESIZED = '../../extracted/miss_collection/gray'

    assert os.path.exists(PATH_INPUT_DIR)
    assert os.path.exists(os.path.dirname(PATH_SAVE_DIR))
    if os.path.exists(PATH_SAVE_DIR)==False: os.mkdir(PATH_SAVE_DIR)
    if os.path.exists(PATH_TO_RESIZED)==False: os.mkdir(PATH_TO_RESIZED)

    input_output_save_dict = make_save_paths(PATH_INPUT_DIR, PATH_SAVE_DIR)

    for path_input, path_save in input_output_save_dict.items():
        face_extract.main_procedure(imagefile_name=path_input, path_to_save=path_save, path_to_resized=PATH_TO_RESIZED)


def boys_face_process():
    PATH_INPUT_DIR = '../../extracted/mr_collection/original_pic'
    PATH_SAVE_DIR = '../../extracted/mr_collection/face'
    PATH_TO_RESIZED = '../../extracted/mr_collection/gray'

    assert os.path.exists(PATH_INPUT_DIR)
    assert os.path.exists(os.path.dirname(PATH_SAVE_DIR))
    if os.path.exists(PATH_SAVE_DIR)==False: os.mkdir(PATH_SAVE_DIR)
    if os.path.exists(PATH_TO_RESIZED)==False: os.mkdir(PATH_TO_RESIZED)

    input_output_save_dict = make_save_paths(PATH_INPUT_DIR, PATH_SAVE_DIR)

    for path_input, path_save in input_output_save_dict.items():
        face_extract.main_procedure(imagefile_name=path_input, path_to_save=path_save, path_to_resized=PATH_TO_RESIZED)


if __name__ == '__main__':
    #example_usage()
    girls_face_process()
    boys_face_process()