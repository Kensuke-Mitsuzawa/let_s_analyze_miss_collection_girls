#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

from settings import *
from bs4 import BeautifulSoup
from bs4.element import Tag
import urllib2
import re
import time
import sys
from collections import namedtuple

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


    def parse_top_html(self, top_html):
        """This method get parse top page.

        :param top_html:
        :return:
        """
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


    def __parge_member_abstract(self, univ_name, member_node):
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
        assert isinstance(university_objects, list)
        for univ_obj in university_objects: assert isinstance(univ_obj, TopUnivInfo)

        stack = []
        for univ_obj in university_objects:
            url_link = self.root_url + univ_obj.link_univ_page
            univ_top_html = self.__get_html_page(url_link)
            self.parge_univ_member_page(univ_name=univ_obj.univ_name, univ_member_page_html=univ_top_html)
            time.sleep(wait_time)

        return stack











