#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import unittest
import json
import codecs

from analysis.dimension_reduction.modules.data_loader_documet import *


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







def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDocumentDataLoader)

    return suite