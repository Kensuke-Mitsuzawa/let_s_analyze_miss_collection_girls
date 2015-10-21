#! -*- coding: utf-8 -*-

import document_reduction
from modules.data_loader_documet import SubProfiles
from modules.data_loader_picture import PictureDataLoader
from modules.space_converter_with_deep_learning import SpaceConverterDeepFeature
from modules.space_converter_with_deep_learning import SpaceConverterDeepFeaturePyLearn2
from modules import reduction_core
import json
import codecs
import pickle
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
                                  name_rubi=member_profile_dict['name_rubi'], university=member_profile_dict['univ_name'],
                                  profile_url=member_profile_dict['profile_page_url'])

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


def prepare_picture_matrix_with_deepNN_features(path_to_members_info_json, path_to_trained_model_pickle,
                                                path_to_datasource_dir, project_name, vector_numbers_index, reduction_mode):
    """This method create feature Embedded matrix. Thus, feature space is already converted into new space made with deepLeanrning.
    This method is only for pylearn2 model.

    :param path_to_trained_model_pickle:
    :param vector_numbers_index:
    :return:
    """
    assert isinstance(vector_numbers_index, list)
    assert os.path.exists(path_to_trained_model_pickle)
    assert os.path.exists(path_to_datasource_dir)
    if not reduction_mode in ['t-sne', 'pca']: raise SystemError('reduction mode is {t-sne, pca}')

    members_profiles = json.loads(codecs.open(path_to_members_info_json, 'r', 'utf-8').read())
    name_rubi_photo_url_obj = document_reduction.__make_name_prof_url_object(members_profiles=members_profiles)
    name_blog_url_obj = document_reduction.__make_name_blog_link_url_object(members_profiles=members_profiles)
    name_sub_prof_mapper = {member_dict_obj['name_rubi']: make_member_profile(member_dict_obj) for member_dict_obj in members_profiles}


    path_to_index_datasource = os.path.join(path_to_datasource_dir, '{}_index_data.json'.format(project_name))
    path_to_datasource_npy = os.path.join(path_to_datasource_dir, '{}.npy'.format(project_name))

    assert os.path.exists(path_to_index_datasource)
    assert os.path.exists(path_to_datasource_npy)

    index_datasource_mapper = json.loads(codecs.open(path_to_index_datasource, 'r', 'utf-8').read())
    datasource_ndarray = numpy.load(path_to_datasource_npy)

    member_name_detector = lambda path_to_main_prof: os.path.splitext(os.path.basename(path_to_main_prof))[0].replace(u'_main', u'')
    main_prof_detector = lambda path_to_pics: '_main.jpg' in path_to_pics
    index_main_prof_mapper = {
        member_name_detector(member_name): int(index)
        for index, member_name in index_datasource_mapper.items()
        if main_prof_detector(member_name)
    }

    space_convert_obj = SpaceConverterDeepFeaturePyLearn2(path_to_trained_model_pickle=path_to_trained_model_pickle,
                                                          data_source_matrix=datasource_ndarray)
    selected_vectors = space_convert_obj.select_feature_vectors(vector_index_numbers=vector_numbers_index)
    converted_matrix = space_convert_obj.space_convert(feature_vectors=selected_vectors)
    assert isinstance(converted_matrix, numpy.ndarray)

    name_vector_mapper = {
        member_name: converted_matrix[index]
        for member_name, index in index_main_prof_mapper.items()
    }

    if reduction_mode=='t-sne':
        low_dim_matrix = reduction_core.execute_tsne(ndarray_matrix=numpy.array([vec for vec in name_vector_mapper.values()]),
                                                     target_dims=2, logger=logger, svd=False)
    elif reduction_mode=='pca':
        low_dim_matrix = reduction_core.call_pca(ndarray_matrix=numpy.array([vec for vec in name_vector_mapper.values()]),
                                                     low_dims=2, logger=logger, normalize=False)
    else:
        raise SystemError('must be {t-sne, pca}')


    index_subprof_mapper = make_index_subprof_mapper(name_subprof_mapper=name_sub_prof_mapper,
                                                     index_name_mapper={
                                                         new_index: name
                                                         for new_index, name
                                                         in enumerate(index_main_prof_mapper.keys())
                                                         })
    member_position_map = document_reduction.make_position_objects(members_index_map=index_subprof_mapper,
                                             name_rubi_photo_url_obj=name_rubi_photo_url_obj,
                                             name_blog_url_obj=name_blog_url_obj,
                                             low_dim_matrix=low_dim_matrix)


    return member_position_map



