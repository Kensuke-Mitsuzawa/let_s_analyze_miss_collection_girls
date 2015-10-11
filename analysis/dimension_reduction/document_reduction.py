#! -*- coding: utf-8 -*-
import codecs
import json
import os
import numpy

from analysis.dimension_reduction.modules.data_loader_documet import DocumentDataLoader
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

PATH_PROFILE_JSON = '../../extracted/miss_collection/miss_member.json'


def prepare_all_members_matrix():
    """ミスコン出場者の行列を生成する


    :return:
    """
    assert os.path.exists(PATH_PROFILE_JSON)
    members_profiles = json.loads(codecs.open(PATH_PROFILE_JSON, 'r', 'utf-8').read())
    document_loader_obj = DocumentDataLoader()
    members_matrix, members_index_map = document_loader_obj.make_all_members_matrix(members_profiles)
    assert isinstance(members_matrix, numpy.ndarray)
    assert isinstance(members_index_map, dict)

    low_dim_matrix_svd = reduction_core.call_svd(members_matrix, 2, logger)
    low_dim_matrix_tsne = reduction_core.execute_tsne(members_matrix, 2, logger)



if __name__ == '__main__':
    prepare_all_members_matrix()