#! -*- coding: utf-8 -*-
from datetime import date, timedelta
import re

import numpy
import random
from analysis.dimension_reduction.modules.JapaneseTokenizers.JapaneseTokenizer.mecab_wrapper.mecab_wrapper import MecabWrapper
from models.question_answer import QuestionAnswerModel

__author__ = 'kensuke-mi'


class ProfileFeatures(object):
    def __init__(self, sub_profile_obj, question_answer_obj, question_id_mapper):
        assert isinstance(sub_profile_obj, SubProfiles)
        assert isinstance(question_answer_obj, QuestionAnswerModel)
        assert isinstance(question_id_mapper, dict)
        self.sub_profile = sub_profile_obj
        self.question_answer = question_answer_obj
        self.question_id = question_id_mapper

    def make_qa_features(self):
        features = {}
        for question, words in self.question_answer.question_answers.items():
            question_id = self.question_id[question]
            for w in words:
                features[u'question_no{}_word_{}'.format(question_id, w)] = 1

        return features

    def make_sub_prof_features(self):
        features = {}
        features[u'age'] = self.sub_profile.age
        features[u'height'] = self.sub_profile.height
        features[u'grade'] = self.sub_profile.grade
        #features[u'major'] = self.sub_profile.major

        return features

    def __repr__(self):
        return 'ProfileFeatures'


class SubProfiles(object):
    def __init__(self, birth_date, birth_place, height, major, name, name_rubi, university, profile_url):
        self.birth_date = birth_date
        today = date.today()
        self.age = self.yearbirthday(b=self.__split_birth_day(), y=today)
        self.birth_place = birth_place
        self.height = float(height.replace(u'cm', u''))

        self.name = name
        self.name_rubi = name_rubi
        self.university = university
        self.profile_url = profile_url

        if major == '':
            self.major = 'unknown'
            self.grade = 0
        else:
            self.major = self.__split_major_and_grade(major)[0]
            self.grade = self.__split_major_and_grade(major)[1]

    def __split_major_and_grade(self, major_and_grade):
        assert isinstance(major_and_grade, unicode)
        try:
            major = re.sub(ur'^(.+)(\d.+)', repl=r'\1', string=major_and_grade)
            grade = re.sub(ur'^(.+)(\d.+)', repl=r'\2', string=major_and_grade)
            grade = int(grade.replace(u'年', u''))
            return major, grade
        except:
            SystemError()

    def __split_birth_day(self):
        if u'年' in self.birth_date:
            year, rest = self.birth_date.split(u'年')
            month, rest = rest.split(u'月')
            day = rest.replace(u'日', u'')
        else:
            # 年齢不詳な場合は、いまの年にしておく。そうしたら、年齢が０になるはず
            month, rest = self.birth_date.split(u'月')
            day = rest.replace(u'日', u'')
            #year = date.today().year - random.randint(18, 23)
            year = 2015

        return date(int(year), int(month), int(day))

    def yearbirthday(self, b, y):
        assert isinstance(b, date)
        assert isinstance(y, date)

        try:
            adjust = b.replace(year=y.year)
        except ValueError:
            b += timedelta(days=1)
            adjust = b.replace(year=y.year)

        age = y.year - b.year
        if b < adjust:
            age -= 1

        return age

    def __repr__(self):
        return 'SubProfile object'


class DocumentDataLoader(object):
    def __init__(self):
        self.__pre_setting()
        self.feature_id_mapper = {}
        self.question_id_mapper = {}


    def __pre_setting(self):
        osType = "mac"
        self.setStop = set([u"の", u"が"])
        self.setPos = set([u"名詞", u'形容詞'])
        self.mecab_wrapper = MecabWrapper(dictType='neologd', osType=osType)

    def update_question_id_mapper(self, question_answer_dict_obj):
        assert isinstance(question_answer_dict_obj, dict)
        for question_content in question_answer_dict_obj.keys():
            if not question_content in self.question_id_mapper:
                if len(self.question_id_mapper) == 0:
                    max_id = 0
                else:
                    max_id = max(self.question_id_mapper.values())

                self.question_id_mapper[question_content] = max_id + 1

    def make_qa_model(self, person_name, question_answer_dict_obj):
        assert isinstance(question_answer_dict_obj, dict)
        self.update_question_id_mapper(question_answer_dict_obj)
        qestion_answer_obj = QuestionAnswerModel(question_answer_dict_obj, MecabTokenizer=self.mecab_wrapper,
                            setStopwords=self.setStop, setPos=self.setPos, personname=person_name)

        return qestion_answer_obj

    def make_member_profile(self, member_profile_dict):
        assert isinstance(member_profile_dict, dict)
        assert member_profile_dict.has_key('QA')

        question_answer_obj = self.make_qa_model(member_profile_dict['name'], member_profile_dict['QA'])
        sub_profile_obj = SubProfiles(birth_date=member_profile_dict['birth_date'], birth_place=member_profile_dict['birth_place'],
                                      height=member_profile_dict['height'], major=member_profile_dict['major'], name=member_profile_dict['name'],
                                      name_rubi=member_profile_dict['name_rubi'], university=member_profile_dict['univ_name'],
                                      profile_url=member_profile_dict['profile_page_url'])
        profile_features_obj = ProfileFeatures(sub_profile_obj=sub_profile_obj, question_answer_obj=question_answer_obj,
                        question_id_mapper=self.question_id_mapper)
        #features = profile_features_obj.make_string_features()

        return profile_features_obj

    def make_feature_index(self, members_prof_objects):
        assert isinstance(members_prof_objects, list)
        feature_index = []
        for members_prof_obj in members_prof_objects:
            assert isinstance(members_prof_obj, ProfileFeatures)
            feature_index += members_prof_obj.make_qa_features().keys()

        feature_index += members_prof_obj.make_sub_prof_features().keys()
        feature_index = sorted(feature_index, key=lambda x: x[0])
        self.feture_index = feature_index
        return {string_feature: feature_number for feature_number, string_feature in enumerate(feature_index)}

    def make_members_array(self, members_prof_objects, index_number):
        assert isinstance(members_prof_objects, ProfileFeatures)
        assert hasattr(self, "feature_index_mapper")
        assert isinstance(index_number, int)

        numpy_array = numpy.zeros(max(self.feature_index_mapper.values()) + 1)
        qa_features = members_prof_objects.make_qa_features()
        for qa_feature in qa_features:
            numpy_array[self.feature_index_mapper[qa_feature]] = qa_features[qa_feature]
        sub_prof_feature_dict = members_prof_objects.make_sub_prof_features()
        for sub_prof_feature in sub_prof_feature_dict:
            #print self.feature_index_mapper[sub_prof_feature]
            #print sub_prof_feature_dict[sub_prof_feature]
            numpy_array[self.feature_index_mapper[sub_prof_feature]] = sub_prof_feature_dict[sub_prof_feature]
        return numpy_array, index_number, members_prof_objects.sub_profile

    def make_all_members_matrix(self, all_members_profile_dict_obj):
        """This method creates feature matrix of all members.
        And this method returns {index: member_name} object also.

        :param all_members_profile_dict_obj:
        :return:
        """
        assert isinstance(all_members_profile_dict_obj, list)
        members_prof_objects = [
            self.make_member_profile(member_prof_obj)
            for member_prof_obj
            in all_members_profile_dict_obj
        ]
        self.feature_index_mapper = self.make_feature_index(members_prof_objects)

        # This list contains (members_vector, member_index_no, member_sub_profile)
        members_array_tuples = [
            self.make_members_array(members_prof_objects, index_number)
            for index_number, members_prof_objects
            in enumerate(members_prof_objects)
        ]
        members_index_map = {
            info_tuple[1]: info_tuple[2]
            for info_tuple
            in members_array_tuples
        }
        members_arrays = [
            info_tuple[0]
            for info_tuple
            in members_array_tuples
        ]

        members_matrix = numpy.array(members_arrays)

        return  members_matrix, members_index_map