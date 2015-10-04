#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import codecs
import json
import os

import numpy

from analysis.dimension_reduction.modules.data_loader_documet import DocumentDataLoader

PATH_PROFILE_JSON = '../../extracted/miss_collection/miss_member.json'
def prepare_all_members_matrix():
    """ミスコン出場者の行列を生成する


    :return:
    """
    assert os.path.exists(PATH_PROFILE_JSON)
    members_profiles = json.loads(codecs.open(PATH_PROFILE_JSON, 'r', 'utf-8').read())
    document_loader_obj = DocumentDataLoader()
    members_matrix = document_loader_obj.make_all_members_matrix(members_profiles)
    assert isinstance(members_matrix, numpy.ndarray)
    # TODO 素性への変換情報を保存しておくこと



if __name__ == '__main__':
    prepare_all_members_matrix()