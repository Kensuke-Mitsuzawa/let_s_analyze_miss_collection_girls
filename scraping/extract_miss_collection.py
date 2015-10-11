#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
__version__ = '0.1'

from settings import *
from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import ResultSet
import os
import urllib2
import re
import time
import codecs
import json
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

# ----------------------------------------------------------
TopUnivInfo = namedtuple("UnivInfo", "univ_name link_univ_page")
UnivMemberPage = namedtuple("UnivMemberPage", "univ_name link_univ_page html")
#PersonPhotoUrl = namedtuple("PersonPhotoURL", "photo_url person_name")

class PersonPhotoUrl(object):
    def __init__(self, photo_url, person_name):
        self.photo_url = photo_url
        self.person_name = person_name


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
        self.photo_urls = []


# ----------------------------------------------------------
class ExtractPersonInfo(object):
    def __init__(self, root_url, path_to_cache_files):
        assert isinstance(root_url, (unicode, str))
        assert os.path.exists(path_to_cache_files)

        if type(root_url) == str:
            self.root_url = root_url.decode('utf-8')
        else:
            self.root_url = root_url

        self.path_to_cache_files = path_to_cache_files
        if os.path.exists(os.path.join(path_to_cache_files, 'pics'))==False:
            os.mkdir(os.path.join(path_to_cache_files, 'pics'))


    def __checkURL(self, url):
        try:
            f = urllib2.urlopen(url)
            f.close()
            time.sleep(random.randint(wait_time_from, wait_time_to))
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
    def save_univ_pickle_object(self, object):
        path_to_pickle = os.path.join(self.path_to_cache_files, 'universities.pickle')

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

        return path_to_pickle


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

    # -------------------------------------------------------------------------------
    # these methods are to get photo pages
    def __get_link_to_photo_page(self, univInfoTuple):
        """This method gets photo link to each university page

        :param univInfoTuple:
        :return:
        """
        assert isinstance(univInfoTuple, TopUnivInfo)
        link_photos = self.root_url + os.path.join(univInfoTuple.link_univ_page, 'photo')
        if link_photos not in except_pages:
            assert self.__checkURL(link_photos)
            return univInfoTuple.univ_name, link_photos

        else:
            return univInfoTuple.univ_name, None


    def __extract_photo_url_personame(self, photo_node):
        """This method just extracts photo url and name

        :param photo_node:
        :return:
        """
        assert isinstance(photo_node, Tag)

        photo_url = photo_node.find("a").get("href")
        photo_name = photo_node.find("a").get("rel")[0]

        return PersonPhotoUrl(photo_url, photo_name)


    def __person_photo_root(self, person_photos_root_node):
        """This method returns all photo urls in one person

        :param person_photos_root_node:
        :return:
        """
        assert isinstance(person_photos_root_node, Tag)
        photos_nodes = person_photos_root_node.find("ul", class_="photos").find_all("li", class_="photo")
        assert isinstance(photos_nodes, ResultSet)

        person_photo_infos = [
            self.__extract_photo_url_personame(p_node)
            for p_node
            in photos_nodes
        ]
        logging.info(msg=u"Finished extracting photo links of Mr/Ms {}".format(person_photo_infos[0].person_name))

        return person_photo_infos


    def __parse_photo_page(self, university_link_obj):
        """This method returns photoURL and Personname of ALL members in each university pgae. Like this page https://misscolle.com/aoyama2015/photo

        :param university_link_obj:
        :return:
        """
        assert isinstance(university_link_obj, tuple)
        assert isinstance(university_link_obj[0], (str, unicode))
        assert isinstance(university_link_obj[1], (str, unicode))

        members_photos_root_html = self.__get_html_page(university_link_obj[1])
        time.sleep(random.randint(wait_time_from, wait_time_to))

        photo_page_node = BeautifulSoup(members_photos_root_html, "html.parser")

        photo_node_top = photo_page_node.find("div", id="whole").find("div", id="content-wrap")\
            .find("div", id="content-main").find("div", id="contest-main").find("div", id="photo-content").find("ul", id="photo_entries")
        photo_nodes = photo_node_top.find_all('li', class_='photo_entry')
        assert isinstance(photo_nodes, list)

        photo_member_persons = [
            self.__person_photo_root(person_node_root)
            for person_node_root
            in photo_nodes
        ]
        logging.info(msg=u"Finished extracting member photo links in {}".format(university_link_obj[0]))

        return [one_item for member_urls_objects in photo_member_persons for one_item in member_urls_objects]


    def make_photo_links(self, universities):
        """This method creates (photo url, person name) tuple for all persons

        :param universities:
        :return:
        """
        assert isinstance(universities, list)
        photo_links_object = [
            self.__get_link_to_photo_page(university_obj)
            for university_obj
            in universities
        ]
        photo_links_object = [p_obj for p_obj in photo_links_object if p_obj[1] != None]

        all_person_photo_urls = [
            self.__parse_photo_page(university_photo_link_tuple)
            for university_photo_link_tuple
            in photo_links_object
        ]
        assert isinstance(all_person_photo_urls, list)
        for l in all_person_photo_urls: assert isinstance(l, list)

        self.all_photo_urls = [person_obj for per_university in all_person_photo_urls for person_obj in per_university]
        return self.all_photo_urls


    def save_photo_links_pickle(self):
        path_to_pickle = os.path.join(self.path_to_cache_files, 'photo_links.pickle')

        assert os.path.exists(os.path.dirname(path_to_pickle))
        assert hasattr(self, 'all_photo_urls')

        """
        converted_object = [
            {
                "photo_url": PersonPhotoUrl.photo_url,
                "person_name":  PersonPhotoUrl.person_name
            }
            for PersonPhotoUrl
            in self.all_photo_urls
        ]"""
        f = open(path_to_pickle, "w")
        pickle.dump(self.all_photo_urls, f)
        f.close()

        return path_to_pickle

    # -------------------------------------------------------------------------------
    def make_person_information(self, list_of_abstract_obj):
        """This method fetches personal information from

        :param list_of_abstract_obj:
        :return:
        """
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

        self.person_information = stack
        return stack


    def save_persons_information_pickle(self, member_profile_info):
        assert isinstance(member_profile_info, list)
        assert os.path.exists(self.path_to_cache_files)
        path_to_pickle = os.path.join(self.path_to_cache_files, 'persons_information.pickle')
        self.save_pickle_object(path_to_pickle=path_to_pickle, object=member_profile_info)

        return path_to_pickle

    # -------------------------------------------------------------------------------
    def __reconstruct_person_information(self, person_information_object):
        assert isinstance(person_information_object, MemberProfiles)

        person_name = re.sub(ur'\s', u'', person_information_object.abstract.member_name)

        return person_name


    def __reconstruct_photo_object(self, all_photo_urls):
        """This method remake the structure of photo link objects. Key is person name and value is urls to photos

        :param all_photo_urls:
        :return:
        """
        assert isinstance(all_photo_urls, list)
        name_index_dict = {}

        for photo_url_obj in all_photo_urls:
            assert isinstance(photo_url_obj, PersonPhotoUrl)
            person_name = re.sub(ur'\s', u'', photo_url_obj.person_name)
            if name_index_dict.has_key(person_name):
                name_index_dict[person_name].append(photo_url_obj.photo_url)
            else:
                name_index_dict[person_name] = [photo_url_obj.photo_url]

        return name_index_dict


    def merge_person_info_photo_url(self, person_information, all_photo_urls):
        """This method merge して、新しい情報を返す

        :return:
        """
        assert isinstance(person_information, list)
        assert isinstance(all_photo_urls, list)


        name_index_perosn_dict = {
            self.__reconstruct_person_information(person_information_object): person_information_object
            for person_information_object
            in person_information
        }
        name_index_photo_dict = self.__reconstruct_photo_object(all_photo_urls)

        for name, person_info_obj in name_index_perosn_dict.items():
            assert isinstance(person_info_obj, MemberProfiles)
            try:
                photo_urls = name_index_photo_dict[name]
                person_info_obj.photo_urls = photo_urls
                name_index_perosn_dict[name] = person_info_obj
            except KeyError:
                logging.warning(msg=u'Person name {} is not existing in name_index_photo_dict. But keep processing'.format(name))

        self.person_index_information = name_index_perosn_dict
        return self.person_index_information
    # -------------------------------------------------------------------------------
    def __download_pics(self, url, path):
        try:
            fp = urllib2.urlopen(url)
            local = open(path, 'wb')
            local.write(fp.read())
            local.close()
            fp.close()
        except urllib2.HTTPError:
            logging.warning(msg=u'{} is invalid URL. Skipped'.format(url))


    def __make_persons_directory(self, path_to_pics_dir, person_name):
        assert os.path.exists(path_to_pics_dir)
        person_s_dir = os.path.join(path_to_pics_dir, person_name)

        if os.path.exists(person_s_dir)==False:
            os.mkdir(person_s_dir)

        return person_s_dir


    def conv_profiles_with_json(self, person_index_information, path_pics_dir):
        assert isinstance(person_index_information, dict)
        assert os.path.exists(path_pics_dir)

        array_object = []
        index_number = 1
        for index_person_name, member_profile in person_index_information.items():

            item = {}
            assert isinstance(member_profile, MemberProfiles)
            item['name'] = member_profile.abstract.member_name
            item['name_rubi'] = member_profile.profile.name_rubi
            item['univ_name'] = member_profile.abstract.univ_name
            item['entry_no'] = member_profile.abstract.entry_no

            item['twitter_link'] = member_profile.abstract.twitter_link
            item['blog_link'] = member_profile.abstract.blog_link

            item['top_profile_photo_url'] = member_profile.abstract.photo_url
            item['photo_urls'] = [self.root_url + url for url in member_profile.photo_urls]

            item['birth_date'] = member_profile.profile.birth_date
            item['birth_place'] = member_profile.profile.birth_place
            item['blood_type'] = member_profile.profile.blood_type
            item['height'] = member_profile.profile.height
            item['major'] = member_profile.profile.major
            item['QA'] = {}


            path_to_persons_pics_dir = self.__make_persons_directory(path_to_pics_dir=path_pics_dir,
                                                                     person_name=member_profile.profile.name_rubi)
            # ----------------------------------------------------------------------
            # download and save top profile picture

            path_top_pic = u'{}.jpg'.format(os.path.join(path_to_persons_pics_dir, member_profile.profile.name_rubi))
            self.__download_pics(url=member_profile.abstract.photo_url, path=path_top_pic)
            time.sleep(random.randint(wait_time_from, wait_time_to))
            # ----------------------------------------------------------------------
            # download and save all profile pictures
            path_to_saved_photos = []
            for photo_index, photo_url in enumerate(member_profile.photo_urls):
                path_to_photo = os.path.join(path_to_persons_pics_dir, u'{}_{}.jpg'.format(member_profile.profile.name_rubi,
                                                                                           photo_index))
                self.__download_pics(url=self.root_url + photo_url, path=path_to_photo)
                path_to_saved_photos.append(path_to_photo)

            # ----------------------------------------------------------------------
            for key_value_tuple in member_profile.QA:
                item['QA'][key_value_tuple[0]] = key_value_tuple[1]

            array_object.append(item)
            logging.info(msg=u'{} of {} is processed'.format(index_number, len(person_index_information)))
            index_number += 1

        return array_object


    def save_result_with_json(self, person_index_information):
        assert os.path.exists(self.path_to_cache_files)
        assert isinstance(person_index_information, dict)

        if os.path.exists(os.path.join(self.path_to_cache_files, 'original_pic'))==False:
            os.mkdir(os.path.join(self.path_to_cache_files, 'original_pic'))


        array_object = self.conv_profiles_with_json(person_index_information=person_index_information,
                                                    path_pics_dir=os.path.join(self.path_to_cache_files, 'original_pic'))

        path_member_json = self
        with codecs.open(os.path.join(self.path_to_cache_files, 'miss_member.json'), 'w', 'utf-8') as f:
            f.write(json.dumps(array_object, indent=4, ensure_ascii=False))

