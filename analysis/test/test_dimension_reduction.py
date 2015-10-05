#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import unittest
import json
import codecs

from analysis.dimension_reduction.modules.data_loader_documet import *
from analysis.dimension_reduction.modules.data_loader_picture import *


class TestDocumentDataLoader(unittest.TestCase):
    def setUp(self):
        self.path_test_json = 'qa_test_document.json'
        self.question_answer_dict_objects = json.loads(codecs.open(self.path_test_json).read())
        self.document_data_load = DocumentDataLoader()

    def test_make_member_matrix(self):
        member_profile_dict = self.question_answer_dict_objects[0]
        profile_obj = self.document_data_load.make_member_profile(member_profile_dict)
        assert isinstance(profile_obj, ProfileFeatures)

    def test_make_all_members_matrix(self):
        self.document_data_load.make_all_members_matrix(self.question_answer_dict_objects)


class TestPictureDataLoader(unittest.TestCase):
    def setUp(self):
        self.list_path_to_files = [
            './pics/Adachi Mako_resized.jpg',
            './pics/Amano Nanami_resized.jpg'
        ]
        self.pic_data_loader_obj = PictureDataLoader(list_path_to_images=self.list_path_to_files)

    def test_make_data_matrix(self):
        # this method returns tuple
        file_index_mapper, data_matrix = self.pic_data_loader_obj.make_data_matrix()
        assert isinstance(file_index_mapper, dict)
        assert isinstance(data_matrix, np.ndarray)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDocumentDataLoader)

    return suite