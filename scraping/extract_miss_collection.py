#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
__version__ = '0.1'

from settings import *
from bs4 import BeautifulSoup
from bs4.element import Tag
import os
import urllib2
import re
import time
import sys
from collections import namedtuple
import pickle
import logging
import random
random.seed(1)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#sys.stderrへ出力するハンドラーを定義
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(formatter)
#rootロガーにハンドラーを登録する
logger.addHandler(sh)

TopUnivInfo = namedtuple("UnivInfo", "univ_name link_univ_page")
UnivMemberPage = namedtuple("UnivMemberPage", "univ_name link_univ_page html")


class MemberAbstractInfo(object):
    def __init__(self, root_url, unive_name, entry_no, photo_url, member_name, prof_link, photo_link, twitter_link, blog_link):
        assert isinstance(unive_name, (str, unicode))
        assert isinstance(entry_no, (str, unicode))
        assert isinstance(member_name, (str, unicode))
        assert isinstance(prof_link, (str, unicode))
        assert isinstance(photo_link, (str, unicode))
        assert isinstance(twitter_link, (str, unicode))
        assert isinstance(blog_link, (str, unicode))

        self.blog_link = blog_link
        self.twitter_link = twitter_link
        self.photo_link = root_url + photo_link
        self.prof_link = root_url + prof_link
        self.photo_url = root_url + photo_url
        self.member_name = member_name
        self.entry_no = entry_no
        self.univ_name = unive_name
    def __repr__(self):
        return "Member Abstract object"


class ProfileInfo(object):
    def __init__(self, birth_date, birth_place, height, blood_type, member_name, member_name_rubi, major):
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.height = height
        self.blood_type = blood_type
        self.name_rubi = member_name_rubi
        self.major = major
    def __repr__(self):
        return "Profile Object"


class MemberProfiles(object):
    def __init__(self, member_abstract_obj, profile_obj, q_a_tuples):
        assert isinstance(member_abstract_obj, MemberAbstractInfo)
        assert isinstance(profile_obj, ProfileInfo)
        assert isinstance(q_a_tuples, list)

        self.abstract = member_abstract_obj
        self.profile = profile_obj
        self.QA = q_a_tuples


class ExtractPersonInfo(object):
    def __init__(self, root_url):
        assert isinstance(root_url, (unicode, str))

        self.root_url = root_url


    def __checkURL(self, url):
        try:
            f = urllib2.urlopen(url)
            f.close()
            return True

        except urllib2.HTTPError:
            print "NotFound:" + url
            return False


    def __get_html_page(self, page_url):
        req = urllib2.Request(page_url)
        req.add_header("User-agent", user_agent)
        top_html_data = urllib2.urlopen(req).read()

        return top_html_data

    def save_pickle_object(self, path_to_pickle, object):
        assert os.path.exists(os.path.dirname(path_to_pickle))
        f = open(path_to_pickle, "w")
        pickle.dump(object, f)
        f.close()
    # -------------------------------------------------------------------------------
    # These methods are for parsing top page
    def save_univ_pickle_object(self, path_to_pickle, object):
        assert os.path.exists(os.path.dirname(path_to_pickle))
        converted_object = [
            {
                "univ_name": univ_tuple.univ_name,
                "univ_link":  univ_tuple.link_univ_page
            }
            for univ_tuple
            in object
        ]
        f = open(path_to_pickle, "w")
        pickle.dump(converted_object, f)
        f.close()


    def parse_top_html(self):
        """This method get parse top page.

        :param top_html:
        :return:
        """
        top_html = self.__get_html_page(page_url=self.root_url)
        assert isinstance(top_html, (str, unicode))
        soup = BeautifulSoup(top_html, "html.parser")

        whole_node = soup.find("div", id="whole")
        main_node = whole_node.find("div", id="content-wrap").find("div", id="content-main")

        contests_nodes = main_node.find("div", id="contests-panel").find("div", id="contests")
        university_nodes = contests_nodes.find_all("div", class_=re.compile(r'^univ'))

        assert isinstance(university_nodes, list)
        univ_page_objects = [
            self.__parse_top_university_node(univ_node)
            for univ_node in university_nodes
        ]

        logging.info(msg=u"finished extracting from top page")
        return univ_page_objects


    def __parse_top_university_node(self, top_university_node):
        """This method parse university nodes in top page.

        :param top_university_node:
        :return:
        """
        assert isinstance(top_university_node, Tag)

        university_name = top_university_node.get("name")
        link_univ_page = top_university_node.find("a").get("href")


        univ_obj_tuple = TopUnivInfo(university_name, link_univ_page)

        return univ_obj_tuple


    # -------------------------------------------------------------------------------
    # These methods are for parsing member page in each university
    def __parge_member_abstract(self, univ_name, member_node):
        """This method extracts member abstract information from university member page
        See https://misscolle.com/kandai2015, as example

        :param univ_name:
        :param member_node:
        :return:
        """
        assert isinstance(univ_name, (str, unicode))
        assert isinstance(member_node, Tag)

        photo_url = member_node.find("div", class_="main-photo").find("img").get("src")
        info_node = member_node.find("div", class_="info")
        entry_no = unicode(info_node.find("span").string)
        member_name = unicode(info_node.find("h3").string)

        prof_link = info_node.find("ul").find("li", class_="profile").find("a").get("href")
        photos_link = info_node.find("ul").find("li", class_="photo").find("a").get("href")

        try:
            twitter_link = info_node.find("div", class_="icon-box").find("a", class_="twitter").get("href")
        except AttributeError:
            twitter_link = u''

        try:
            blog_link = info_node.find("div", class_="icon-box").find("a", class_="blog").get("href")
        except AttributeError:
            blog_link= u''

        member_abst_obj = MemberAbstractInfo(root_url=self.root_url,
                          unive_name=univ_name,
                           entry_no=entry_no,
                           photo_url=photo_url,
                           member_name=member_name,
                           prof_link=prof_link,
                           photo_link=photos_link,
                           twitter_link=twitter_link,
                           blog_link=blog_link)

        return member_abst_obj


    def parge_univ_member_page(self, univ_name, univ_member_page_html):
        """This method pars member top page of each university page.

        :param univ_name:
        :param univ_member_page_html:
        :return:
        """
        assert isinstance(univ_member_page_html, (str, unicode))
        member_page_node = BeautifulSoup(univ_member_page_html, "html.parser")
        content_main_node = member_page_node.find("div", id="whole").find("div", id="content-wrap").find("div", id="content-main")
        entries_node = content_main_node.find("div", id="contest-main").find("div", id="entries")
        summary_node = content_main_node.find("div", id="contest-main").find("div", id="summary")

        member_nodes = entries_node.find_all("div", class_="entry")
        assert isinstance(member_nodes, list)
        member_abstract_nodes = [
            self.__parge_member_abstract(univ_name=univ_name, member_node=member_node)
            for member_node
            in member_nodes
        ]

        return member_abstract_nodes


    def get_university_members_page(self, university_objects):
        """This method make member abstract objects of all university

        :param university_objects:
        :return:
        """
        assert isinstance(university_objects, list)
        for univ_obj in university_objects: assert isinstance(univ_obj, TopUnivInfo)

        stack = []
        for univ_obj in university_objects:
            url_link = self.root_url + univ_obj.link_univ_page
            if url_link in except_pages: continue

            logging.info(msg=u"started university {}".format(univ_obj.univ_name))
            univ_top_html = self.__get_html_page(url_link)
            stack += self.parge_univ_member_page(univ_name=univ_obj.univ_name, univ_member_page_html=univ_top_html)
            logging.info(msg=u"finished university {}".format(univ_obj.univ_name))
            time.sleep(random.randint(wait_time_from, wait_time_to))

        return stack

    # -------------------------------------------------------------------------------
    # These methods are for parsing profile page
    def __parse_dl_node_in_member_prof(self, dl_node):
        assert isinstance(dl_node, Tag)

        dt_node = dl_node.find("dt")
        label_name = unicode(dt_node.find("span", class_="ja").string)
        if label_name == u'生年月日':
            key = u'birthday'
        elif label_name==u'出身地':
            key = u'birthplace'
        elif label_name==u'身長':
            key = u'height'
        elif label_name==u'血液型':
            key = u'bloodtype'
        else:
            raise SystemError("Failed to find key")

        value = unicode(dl_node.find("dd").string)

        return {'key': key, 'value': value}


    def __extract_profile_part(self, member_info_node):
        assert isinstance(member_info_node, Tag)

        profile_node = member_info_node.find("div", id="profile").find("div", id="info")
        member_name = unicode(profile_node.find("h2").string)
        member_name_rubi = unicode(profile_node.find("h2").find("span").string)
        major = unicode(profile_node.find("span", class_="gakubu").string).strip()

        dl_nodes = profile_node.find_all("dl")
        key_values_pairs = [
            self.__parse_dl_node_in_member_prof(dl_node)
            for dl_node in dl_nodes
        ]
        detail_prof_info = {}
        for key_value in key_values_pairs:
            value = key_value['value']
            if key_value['key'] == u'birthday':
                detail_prof_info['birth_day'] = value
            elif key_value['key'] == u'birthplace':
                detail_prof_info['birth_place'] = value
            elif key_value['key'] == u'height':
                detail_prof_info['height'] = value
            elif key_value['key'] == u'bloodtype':
                detail_prof_info['bloodtype'] = value


        profile_object = ProfileInfo(birth_date=detail_prof_info['birth_day'],
                    birth_place=detail_prof_info['birth_place'],
                    height=detail_prof_info['height'],
                    blood_type=detail_prof_info['bloodtype'],
                    member_name=member_name,
                    member_name_rubi=member_name_rubi,
                    major=major)
        return profile_object


    def __extract_topic_QA(self, li_node):
        """This method is sub-function of __extract_topics_part

        :param li_node:
        :return:
        """
        assert isinstance(li_node, Tag)
        key = unicode(li_node.find("h3").string).strip()
        value = unicode(li_node.find("p").string).strip()
        if value==None or value==u'None':
            text = li_node.find("p").text
            value = text.strip().replace('\n', u',')
        return key, value


    def __extract_topics_part(self, topics_node):
        """This method extracts QA from profile page See: https://misscolle.com/kandai2015/profile/1

        :param topics_node:
        :return:
        """
        assert isinstance(topics_node, Tag)
        topics_node = topics_node.find("ul", class_="columns js-masonry").find_all("li", class_=re.compile(r"^column"))
        key_value_tuples = [
            self.__extract_topic_QA(li_node)
            for li_node in topics_node
        ]

        return key_value_tuples


    def parse_member_profile_page(self, member_page_html):
        assert isinstance(member_page_html, (str, unicode))

        member_top_node = BeautifulSoup(member_page_html, "html.parser")
        content_main_node = member_top_node.find("div", id="whole").find("div", id="content-wrap").find("div", id="content-main")
        member_info_node = content_main_node.find("div", id="contest-main")
        topics_node = content_main_node.find("div", id="profile_topics")

        profile_object = self.__extract_profile_part(member_info_node)
        q_a_tuples = self.__extract_topics_part(topics_node)

        return profile_object, q_a_tuples
    # TODO 写真一覧を取得するメソッドを書くこと
    # -------------------------------------------------------------------------------
    def make_person_information(self, list_of_abstract_obj):
        assert isinstance(list_of_abstract_obj, list)
        stack = []
        for index_number, abstract_obj in enumerate(list_of_abstract_obj):
            assert isinstance(abstract_obj, MemberAbstractInfo)
            logging.info(msg=u"started {} of {}.".format(abstract_obj.member_name,
                                                                      abstract_obj.univ_name))
            html_page = self.__get_html_page(abstract_obj.prof_link)
            profile_object, q_a_tuples = self.parse_member_profile_page(html_page)
            member_info = MemberProfiles(member_abstract_obj=abstract_obj,
                                         profile_obj=profile_object,
                                         q_a_tuples=q_a_tuples)
            stack.append(member_info)
            logging.info(msg=u"finished {} of {}. Now {} of {}".format(abstract_obj.member_name,
                                                                      abstract_obj.univ_name,
                                                                      index_number,
                                                                      len(list_of_abstract_obj)))
            time.sleep(random.randint(wait_time_from, wait_time_to))

        return stack


    def __download_pics(self, url, path):
        fp = urllib2.urlopen(url)
        local = open(path, 'wb')
        local.write(fp.read())
        local.close()
        fp.close()


    def conv_profiles_with_json(self, list_of_member_profile, path_pics_dir):
        assert isinstance(list_of_member_profile, list)
        assert os.path.exists(path_pics_dir)

        array_object = []
        for index, member_profile in enumerate(list_of_member_profile):
            item = {}
            assert isinstance(member_profile, MemberProfiles)
            item['name'] = member_profile.abstract.member_name
            item['name_rubi'] = member_profile.profile.name_rubi
            item['univ_name'] = member_profile.abstract.univ_name
            item['entry_no'] = member_profile.abstract.entry_no
            item['twitter_link'] = member_profile.abstract.twitter_link
            item['blog_link'] = member_profile.abstract.blog_link
            item['photo_url'] = member_profile.abstract.photo_url
            item['birth_date'] = member_profile.profile.birth_date
            item['birth_place'] = member_profile.profile.birth_place
            item['blood_type'] = member_profile.profile.blood_type
            item['height'] = member_profile.profile.height
            item['major'] = member_profile.profile.major
            item['QA'] = {}

            path_pic = u'{}.jpg'.format(os.path.join(path_pics_dir, member_profile.profile.name_rubi))
            self.__download_pics(url=member_profile.abstract.photo_url, path=path_pic)
            time.sleep(random.randint(wait_time_from, wait_time_to))
            item['path_pic'] = path_pic

            for key_value_tuple in member_profile.QA:
                item['QA'][key_value_tuple[0]] = key_value_tuple[1]

            array_object.append(item)
            logging.info(msg=u'{} of {} is processed'.format(index, len(list_of_member_profile)))

        return array_object