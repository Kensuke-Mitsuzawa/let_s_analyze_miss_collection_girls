#! -*- coding: utf-8 -*-
from settings import *
import extract_miss_collection
import pickle
from extract_miss_collection import *
import json
import codecs

__author__ = 'kensuke-mi'


def load_pickle_obj(path_to_pickle):
    f = open(path_to_pickle, "r")
    l = pickle.load(f)
    f.close()

    return l


def prepare_miss_collection_info():
    PATH_CACHE_DIR = '../extracted/miss_collection/'


    extract_obj = extract_miss_collection.ExtractPersonInfo(root_url=miss_root_url, path_to_cache_files=PATH_CACHE_DIR)

    """
    # make list of target university links
    universities = extract_obj.parse_top_html()
    assert isinstance(universities, list)
    path_to_univ_list_pickle = extract_obj.save_univ_pickle_object(object=universities)

    # make photo urls of all candidate members
    # this method save photo urls inside object
    all_photo_urls = extract_obj.make_photo_links(universities)
    path_to_photos_list_pickle = extract_obj.save_photo_links_pickle()

    # make abstract information of all candidate members
    member_abstract_objects = extract_obj.get_university_members_page(university_objects=universities)
    assert isinstance(member_abstract_objects, list)

    # make all members' profile data
    member_profile_info = extract_obj.make_person_information(member_abstract_objects)
    assert isinstance(member_profile_info, list)
    path_to_persons_information = extract_obj.save_persons_information_pickle(member_profile_info)
    """

    # merge members profile and photo urls
    all_photo_urls = load_pickle_obj(os.path.join(PATH_CACHE_DIR, 'photo_links.pickle'))
    member_profile_data = load_pickle_obj(os.path.join(PATH_CACHE_DIR, 'persons_information.pickle'))
    profile_photo_urls_merged_object = extract_obj.merge_person_info_photo_url(person_information=member_profile_data,
                                                                               all_photo_urls=all_photo_urls)


    # converts into array and dict format to make it use to save with json
    list_of_items = extract_obj.save_result_with_json(profile_photo_urls_merged_object)


def prepare_mr_collection_info():
    PATH_CACHE_DIR = '../extracted/mr_collection/'


    extract_obj = extract_miss_collection.ExtractPersonInfo(root_url=mr_root_url, path_to_cache_files=PATH_CACHE_DIR)

    """
    # make list of target university links
    universities = extract_obj.parse_top_html()
    assert isinstance(universities, list)
    path_to_univ_list_pickle = extract_obj.save_univ_pickle_object(object=universities)

    # make photo urls of all candidate members
    # this method save photo urls inside object
    all_photo_urls = extract_obj.make_photo_links(universities)
    path_to_photos_list_pickle = extract_obj.save_photo_links_pickle()

    # make abstract information of all candidate members
    member_abstract_objects = extract_obj.get_university_members_page(university_objects=universities)
    assert isinstance(member_abstract_objects, list)

    # make all members' profile data
    member_profile_info = extract_obj.make_person_information(member_abstract_objects)
    assert isinstance(member_profile_info, list)
    path_to_persons_information = extract_obj.save_persons_information_pickle(member_profile_info)
    """

    # merge members profile and photo urls
    all_photo_urls = load_pickle_obj(os.path.join(PATH_CACHE_DIR, 'photo_links.pickle'))
    member_profile_data = load_pickle_obj(os.path.join(PATH_CACHE_DIR, 'persons_information.pickle'))
    profile_photo_urls_merged_object = extract_obj.merge_person_info_photo_url(person_information=member_profile_data,
                                                                               all_photo_urls=all_photo_urls)

    # converts into array and dict format to make it use to save with json
    list_of_items = extract_obj.save_result_with_json(profile_photo_urls_merged_object)


if __name__ == '__main__':
    prepare_miss_collection_info()
    prepare_mr_collection_info()


