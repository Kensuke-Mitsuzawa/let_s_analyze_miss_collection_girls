#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
from settings import *
import extract_miss_collection
import pickle
from extract_miss_collection import *
import json
import codecs

def load_pickle_obj(path_to_pickle):
    f = open(path_to_pickle, "r")
    l = pickle.load(f)
    f.close()

    return l



def prepare_miss_collection_info():
    PATH_UNIV_INDEX_PICKLE = '../extracted/miss_collection/miss_univ_index.pickle'
    PATH_MEMBER_ABST_PICKLE = '../extracted/miss_collection/miss_abstract.pickle'
    PATH_MEMBER_INFO = '../extracted/miss_collection/miss_member.pickle'
    PATH_MEMBER_JSON = '../extracted/miss_collection/miss_member.json'


    extract_obj = extract_miss_collection.ExtractPersonInfo(root_url=miss_root_url)

    """
    universities = extract_obj.parse_top_html()
    assert isinstance(universities, list)
    extract_obj.save_univ_pickle_object(path_to_pickle=PATH_UNIV_INDEX_PICKLE, object=universities)

    member_abstract_objects = extract_obj.get_university_members_page(university_objects=universities)
    assert isinstance(member_abstract_objects, list)
    extract_obj.save_pickle_object(path_to_pickle=PATH_MEMBER_ABST_PICKLE, object=member_abstract_objects)

    member_abstract_objects = load_pickle_obj(PATH_MEMBER_ABST_PICKLE)

    member_profile_info = extract_obj.make_person_information(member_abstract_objects)
    assert isinstance(member_profile_info, list)
    extract_obj.save_pickle_object(path_to_pickle=PATH_MEMBER_INFO, object=member_profile_info)
    """

    member_profile_data = load_pickle_obj(PATH_MEMBER_INFO)
    list_of_items = extract_obj.conv_profiles_with_json(member_profile_data)
    with codecs.open(PATH_MEMBER_JSON, 'w', 'utf-8') as f:
        f.write(json.dumps(list_of_items, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    prepare_miss_collection_info()


