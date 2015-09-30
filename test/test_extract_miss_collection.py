#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import scraping.extract_miss_collection
from scraping.extract_miss_collection import ExtractPersonInfo
from scraping.settings import *
import unittest

class TestExtractPersonInfo(unittest.TestCase):
    def setUp(self):
        self.miss_url_root = miss_root_url
        self.extract_obj = ExtractPersonInfo(root_url=self.miss_url_root)


    def test_parse_top_html(self):
        top_html = self.extract_obj._ExtractPersonInfo__get_html_page(self.miss_url_root)
        univ_parsed_objects = self.extract_obj.parse_top_html(top_html)
        assert isinstance(univ_parsed_objects, list)
        for univ_obj in univ_parsed_objects: assert isinstance(univ_obj, scraping.extract_miss_collection.TopUnivInfo)

        return univ_parsed_objects


    def test_parse_univ_member_page(self):
        univ_name1 = "青山"
        univ_link1 = "https://misscolle.com/aoyama2015"
        univ_html1 = self.extract_obj._ExtractPersonInfo__get_html_page(univ_link1)

        members_objects = self.extract_obj.parge_univ_member_page(univ_name=univ_name1,
                                                                  univ_member_page_html=univ_html1)
        assert isinstance(members_objects, list)
        for member_obj in members_objects: assert isinstance(member_obj, scraping.extract_miss_collection.MemberAbstractInfo)


        univ_name2 = "関大"
        univ_link2 = "https://misscolle.com/kandai2015"
        univ_html2 = self.extract_obj._ExtractPersonInfo__get_html_page(univ_link2)

        members_objects = self.extract_obj.parge_univ_member_page(univ_name=univ_name2,
                                                                  univ_member_page_html=univ_html2)
        assert isinstance(members_objects, list)
        for member_obj in members_objects: assert isinstance(member_obj, scraping.extract_miss_collection.MemberAbstractInfo)


    def test_get_univ_members_page(self):
        univ_parsed_objects = self.test_parse_top_html()
        member_abstract_objects = self.extract_obj.get_university_members_page(university_objects=univ_parsed_objects)
        for member_obj in member_abstract_objects: assert isinstance(member_obj, scraping.extract_miss_collection.MemberAbstractInfo)


    def test_parse_member_profile_page(self):
        test_member1 = 'https://misscolle.com/kandai2015/profile/1'
        test_member_html_1 = self.extract_obj._ExtractPersonInfo__get_html_page(test_member1)
        self.extract_obj.parse_member_profile_page(member_page_html=test_member_html_1)






def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestExtractPersonInfo)

    return suite