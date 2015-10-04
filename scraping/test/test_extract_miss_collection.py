#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import scraping.extract_miss_collection
from scraping.extract_miss_collection import ExtractPersonInfo
import scraping.extract_miss_collection
from scraping.settings import *
import unittest

class TestExtractPersonInfo(unittest.TestCase):
    def setUp(self):
        self.miss_url_root = miss_root_url
        self.extract_obj = ExtractPersonInfo(root_url=self.miss_url_root)


    def test_parse_top_html(self):
        top_html = self.extract_obj._ExtractPersonInfo__get_html_page(self.miss_url_root)
        univ_parsed_objects = self.extract_obj.parse_top_html()
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


        univ_name3 = "大阪府立大学"
        univ_link3 = "https://misscolle.com/abeno2015"
        univ_html3 = self.extract_obj._ExtractPersonInfo__get_html_page(univ_link3)

        members_objects = self.extract_obj.parge_univ_member_page(univ_name=univ_name3,
                                                                  univ_member_page_html=univ_html3)
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

        test_member2 = 'https://misscolle.com/rits2015/profile/2'
        test_member_html_2 = self.extract_obj._ExtractPersonInfo__get_html_page(test_member2)
        self.extract_obj.parse_member_profile_page(member_page_html=test_member_html_2)


    def test_parse_photo_page(self):
        test_university_object = scraping.extract_miss_collection.TopUnivInfo(u"青山学院大学", u"https://misscolle.com/aoyama2015")
        photo_url_object = self.extract_obj._ExtractPersonInfo__get_link_to_photo_page(test_university_object)
        list_path_photo_objects = self.extract_obj._ExtractPersonInfo__parse_photo_page(photo_url_object)

        assert isinstance(list_path_photo_objects, list)
        for ob in list_path_photo_objects:
            print ob
            assert isinstance(ob, scraping.extract_miss_collection.PersonPhotoUrl)
            assert len(ob)==2
            print ob[0], ob[1]


    def test_make_photo_links(self):
        test_university_object = [scraping.extract_miss_collection.TopUnivInfo(u"青山学院大学", u"https://misscolle.com/aoyama2015"),
                                  scraping.extract_miss_collection.TopUnivInfo(u"慶應義塾大学", u"https://misscolle.com/keiosfc2015")]
        assert isinstance(test_university_object, list)
        list_all_person_photo_urls = self.extract_obj.make_photo_links(test_university_object)
        assert isinstance(list_all_person_photo_urls, list)
        for obj in list_all_person_photo_urls: assert isinstance(obj, tuple)




def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestExtractPersonInfo)

    return suite