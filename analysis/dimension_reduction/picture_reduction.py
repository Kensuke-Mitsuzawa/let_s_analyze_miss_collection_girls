#! -*- coding: utf-8 -*-

import document_reduction
from modules.data_loader_documet import SubProfiles
from modules.data_loader_picture import PictureDataLoader
from modules.space_converter_with_deep_learning import SpaceConverterDeepFeature
from modules import reduction_core
import json
import codecs
import glob
import re
import os
import numpy
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)

__author__ = 'kensuke-mi'

PATH_TO_PICS_DIR = '../../extracted/miss_collection/gray'
PATH_TO_SAVE_PICKLE = './data_directory/picture_matrix_obj.pickle'
PATH_TO_INPUT_JSON = '../../extracted/miss_collection/miss_member.json'


def make_path_pic_list(path_input_dir, suffix='*jpg', only_main_pic=True):
    path_list = []
    for path_to_pic in glob.glob('{}/{}'.format(path_input_dir, suffix)):
        if only_main_pic==True and re.findall(r'.*\d', path_to_pic)==[]:
            path_list.append(path_to_pic)
        elif only_main_pic==False:
            path_list.append(path_to_pic)

    return path_list


def make_member_profile(member_profile_dict):
    """This method creates {name: sub-profile} object

    :param member_profile_dict:
    :return:
    """
    assert isinstance(member_profile_dict, dict)
    assert member_profile_dict.has_key('QA')

    sub_profile_obj = SubProfiles(birth_date=member_profile_dict['birth_date'], birth_place=member_profile_dict['birth_place'],
                                  height=member_profile_dict['height'], major=member_profile_dict['major'], name=member_profile_dict['name'],
                                  name_rubi=member_profile_dict['name_rubi'], university=member_profile_dict['univ_name'])

    return sub_profile_obj


def make_index_subprof_mapper(name_subprof_mapper, index_name_mapper):
    """This method makes correspondence between {index: name} and {name: sub-prof-object}

    :param name_subprof_mapper:
    :param index_name_mapper:
    :return:
    """

    assert isinstance(name_subprof_mapper, dict)
    assert isinstance(index_name_mapper, dict)

    index_subprof_mapper = {}
    for index, name in index_name_mapper.items():
        index_subprof_mapper[index] = name_subprof_mapper[name]

    return index_subprof_mapper


def prepare_picture_data_matrix(path_input_dir, path_to_save_pickle):
    """This method creates feature matrix from set of pictures

    :param path_input_dir:
    :param path_to_save_pickle:
    :return:
    """
    assert os.path.exists(path_input_dir)
    assert os.path.exists(os.path.dirname(path_to_save_pickle))

    list_path_to_pic_file = make_path_pic_list(path_input_dir, only_main_pic=True)
    pic_data_loader_obj = PictureDataLoader(list_path_to_images=list_path_to_pic_file)
    path_index_mapper, picture_data_matrix = pic_data_loader_obj.make_data_matrix()
    pic_data_loader_obj.save_into_pickle(path_pickle_file=path_to_save_pickle)

    return path_index_mapper, picture_data_matrix


def picture_reduction_normal_tsne(path_input_dir, path_to_input_json, path_to_save_pickle):
    """This method creates member_position_map object which is input of scatter object.

    :param path_input_dir:
    :param path_to_input_json:
    :param path_to_save_pickle:
    :return:
    """
    assert os.path.exists(path_input_dir)
    assert os.path.exists(path_to_input_json)
    assert os.path.exists(os.path.dirname(path_to_save_pickle))

    members_profiles = json.loads(codecs.open(path_to_input_json, 'r', 'utf-8').read())
    name_rubi_photo_url_obj = document_reduction.__make_name_prof_url_object(members_profiles=members_profiles)
    name_blog_url_obj = document_reduction.__make_name_blog_link_url_object(members_profiles=members_profiles)
    name_sub_prof_mapper = {member_dict_obj['name_rubi']: make_member_profile(member_dict_obj) for member_dict_obj in members_profiles}

    path_index_mapper, picture_data_matrix = prepare_picture_data_matrix(path_input_dir, path_to_save_pickle)
    name_extractor = lambda x: x.replace('_main.jpg', '')
    index_name_mapper = {index: name_extractor(os.path.basename(path)) for index, path in path_index_mapper.items()}
    index_subprof_mapper = make_index_subprof_mapper(name_subprof_mapper=name_sub_prof_mapper, index_name_mapper=index_name_mapper)

    low_dim_matrix = reduction_core.execute_tsne(ndarray_matrix=picture_data_matrix, target_dims=2, logger=logger, svd=True)

    member_position_map = document_reduction.make_position_objects(members_index_map=index_subprof_mapper,
                                             name_rubi_photo_url_obj=name_rubi_photo_url_obj,
                                             name_blog_url_obj=name_blog_url_obj,
                                             low_dim_matrix=low_dim_matrix)
    return member_position_map


def prepare_picture_matrix_with_trained_features(path_to_trained_model_pickle, vector_numbers_index):
    """This method create feature Embedded matrix. Thus, feature space is already converted into new space made with deepLeanrning.

    :param path_to_trained_model_pickle:
    :param vector_numbers_index:
    :return:
    """
    # TODO deep learningで素性を作る時点で、入力matrixのindexと人物の対応関係は保持しておかなくてはいけない。このメソッドの入力はdeepNNモデルの入力と同一だから
    assert isinstance(vector_numbers_index, list)
    assert os.path.exists(path_to_trained_model_pickle)

    space_convert_obj = SpaceConverterDeepFeature(path_to_trained_model_pickle=path_to_trained_model_pickle)
    selected_vectors = space_convert_obj.select_feature_vectors(vector_index_numbers=vector_numbers_index)
    converted_matrix = space_convert_obj.space_convert(feature_vectors=selected_vectors)
    assert isinstance(converted_matrix, numpy.ndarray)

if __name__ == '__main__':
    path_to_pic_tsne_result = '../../visualization/data_for_visual/pics_tsne_obj.json'
    position_map_picture_tsne = picture_reduction_normal_tsne(PATH_TO_PICS_DIR, PATH_TO_INPUT_JSON, PATH_TO_SAVE_PICKLE)
    with codecs.open(path_to_pic_tsne_result, 'w', 'utf-8') as f:
        f.write(json.dumps(position_map_picture_tsne, indent=4, ensure_ascii=False))

    #path_to_trained_model_pickle = '../test/relu_2layer_simple_test.pickle'


