#! -*- coding: utf-8 -*-
import codecs
import json
import os
import numpy

from analysis.dimension_reduction.modules.data_loader_documet import DocumentDataLoader
from modules.data_loader_documet import SubProfiles
import modules.reduction_core as reduction_core
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)

__author__ = 'kensuke-mi'


def __make_name_prof_url_object(members_profiles):
    assert isinstance(members_profiles, list)
    member_rubi_url_obj = {
        member_obj['name_rubi']: member_obj['top_profile_photo_url']
        for member_obj
        in members_profiles
    }
    return member_rubi_url_obj


def __make_name_blog_link_url_object(members_profiles):
    assert isinstance(members_profiles, list)
    member_blog_link_obj = {
        member_obj['name_rubi']: member_obj['blog_link']
        for member_obj
        in members_profiles
    }
    return member_blog_link_obj


def __genarate_position_obj(member_index, member_sub_prof_obj, photo_url, blog_url, profile_url, member_position_vec):
    """This method generate one member position object

    :param member_index:
    :param member_sub_prof_obj:
    :param member_position_vec:
    :return:
    """
    assert isinstance(member_index, int)
    #assert isinstance(member_sub_prof_obj, SubProfiles)
    assert isinstance(member_position_vec, numpy.ndarray)
    assert isinstance(photo_url, (str, unicode))

    position_object = {}
    position_object['position_vector'] = member_position_vec.tolist()
    position_object['member_index'] = member_index
    position_object['member_name'] = member_sub_prof_obj.name
    position_object['member_name_rubi'] = member_sub_prof_obj.name_rubi
    position_object['age'] = member_sub_prof_obj.age
    position_object['university'] = member_sub_prof_obj.university
    position_object['major'] = member_sub_prof_obj.major
    position_object['height'] = member_sub_prof_obj.height
    position_object['grade'] = member_sub_prof_obj.grade
    position_object['photo_url'] = photo_url
    position_object['blog_url'] = blog_url
    position_object['profile_url'] = profile_url

    return position_object


def make_position_objects(members_index_map, name_rubi_photo_url_obj, name_blog_url_obj, low_dim_matrix):
    """This method generates following object.
    {
        member_name_rubi: {
            'position_vector': list,
            'member_index': int,
            'age': int,
            'grade': int,
            'height': float,
            'major': str,
            'member_name': str,
            'member_name_rubi': str,
            'photo_url': str,
            'university': str
        }
    }

    :param members_index_map:
    :param name_rubi_photo_url_obj:
    :param low_dim_matrix:
    :return:
    """
    assert isinstance(members_index_map, dict)
    assert isinstance(low_dim_matrix, numpy.ndarray)
    assert isinstance(name_blog_url_obj, dict)
    assert isinstance(name_rubi_photo_url_obj, dict)

    members_position_maps = {}
    for member_index, member_sub_prof in members_index_map.items():
        assert hasattr(member_sub_prof, "name_rubi")
        position_object = __genarate_position_obj(member_index=member_index,
                                                  member_sub_prof_obj=member_sub_prof,
                                                  member_position_vec=low_dim_matrix[member_index],
                                                  photo_url=name_rubi_photo_url_obj[member_sub_prof.name_rubi],
                                                  blog_url=name_blog_url_obj[member_sub_prof.name_rubi],
                                                  profile_url=member_sub_prof.profile_url)
        members_position_maps[member_sub_prof.name_rubi] = position_object

    return members_position_maps



def prepare_all_members_matrix(PATH_PROFILE_JSON):
    """ミスコン出場者の行列を生成する


    :return:
    """
    assert os.path.exists(PATH_PROFILE_JSON)
    members_profiles = json.loads(codecs.open(PATH_PROFILE_JSON, 'r', 'utf-8').read())
    document_loader_obj = DocumentDataLoader()
    members_matrix, members_index_map = document_loader_obj.make_all_members_matrix(members_profiles)
    assert isinstance(members_matrix, numpy.ndarray)
    assert isinstance(members_index_map, dict)

    low_dim_matrix_svd = reduction_core.call_svd(members_matrix, 2, logger, normalize=True)
    low_dim_matrix_tsne = reduction_core.execute_tsne(members_matrix, 2, logger, normalize=True)

    name_rubi_photo_url_obj = __make_name_prof_url_object(members_profiles=members_profiles)
    name_blog_url_obj = __make_name_blog_link_url_object(members_profiles=members_profiles)


    members_position_svd_maps = make_position_objects(members_index_map=members_index_map,
                                                      name_rubi_photo_url_obj=name_rubi_photo_url_obj,
                                                      low_dim_matrix=low_dim_matrix_svd,
                                                      name_blog_url_obj=name_blog_url_obj)
    members_position_tsne_maps =  make_position_objects(members_index_map=members_index_map,
                                                        name_rubi_photo_url_obj=name_rubi_photo_url_obj,
                                                        low_dim_matrix=low_dim_matrix_tsne,
                                                        name_blog_url_obj=name_blog_url_obj)
    assert isinstance(members_position_svd_maps, dict)
    assert isinstance(members_position_tsne_maps, dict)

    return members_position_svd_maps, members_position_tsne_maps


def generate_girls_postion_information():
    PATH_TO_SAVE_RESULT_DIR = '../../visualization/data_for_visual/'
    PATH_PROFILE_JSON = '../../extracted/miss_collection/miss_member.json'

    path_to_save_document_svd_result = os.path.join(PATH_TO_SAVE_RESULT_DIR, 'miss_document_svd_obj.json')
    path_to_save_document_tsne_result = os.path.join(PATH_TO_SAVE_RESULT_DIR, 'miss_document_tsne_obj.json')
    assert os.path.exists(os.path.dirname(path_to_save_document_svd_result))
    assert os.path.exists(os.path.dirname(path_to_save_document_tsne_result))

    members_position_svd_maps, members_position_tsne_maps = prepare_all_members_matrix(PATH_PROFILE_JSON)
    with codecs.open(path_to_save_document_svd_result, 'w', 'utf-8') as f:
        f.write(json.dumps(members_position_svd_maps, ensure_ascii=False, indent=4))

    with codecs.open(path_to_save_document_tsne_result, 'w', 'utf-8') as f:
        f.write(json.dumps(members_position_tsne_maps, ensure_ascii=False, indent=4))


def generate_boys_postion_information():
    PATH_TO_SAVE_RESULT_DIR = '../../visualization/data_for_visual/'
    PATH_PROFILE_JSON = '../../extracted/mr_collection/miss_member.json'

    path_to_save_document_svd_result = os.path.join(PATH_TO_SAVE_RESULT_DIR, 'mr_document_svd_obj.json')
    path_to_save_document_tsne_result = os.path.join(PATH_TO_SAVE_RESULT_DIR, 'mr_document_tsne_obj.json')
    assert os.path.exists(os.path.dirname(path_to_save_document_svd_result))
    assert os.path.exists(os.path.dirname(path_to_save_document_tsne_result))

    members_position_svd_maps, members_position_tsne_maps = prepare_all_members_matrix(PATH_PROFILE_JSON)
    with codecs.open(path_to_save_document_svd_result, 'w', 'utf-8') as f:
        f.write(json.dumps(members_position_svd_maps, ensure_ascii=False, indent=4))

    with codecs.open(path_to_save_document_tsne_result, 'w', 'utf-8') as f:
        f.write(json.dumps(members_position_tsne_maps, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    generate_girls_postion_information()
    generate_boys_postion_information()