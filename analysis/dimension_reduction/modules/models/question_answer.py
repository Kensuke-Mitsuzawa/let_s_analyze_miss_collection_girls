#! -*- coding: utf-8 -*-
from ..JapaneseTokenizers.JapaneseTokenizer.mecab_wrapper.mecab_wrapper import MecabWrapper
__author__ = 'kensuke-mi'


class QuestionAnswerModel(object):

    def __init__(self, question_answer, MecabTokenizer, setStopwords, setPos, personname):
        assert isinstance(MecabTokenizer, MecabWrapper)
        assert isinstance(question_answer, dict)

        self._MecabTokenizer = MecabTokenizer
        self._setStop = setStopwords
        self._setPos = setPos
        question_words = self.make_question_answer_words(question_answer)
        self.question_answers = self.__removeStopWords(question_words)
        self.person_name = personname

    def make_question_answer_words(self, question_answer):
        assert isinstance(question_answer, dict)
        question_words = {
            question: self.__tokenize(text=answer)
            for question, answer
            in question_answer.items()
        }
        return question_words

    def __tokenize(self, text):
        return self._MecabTokenizer.tokenize(text.strip(), is_feature=True)

    def __filter_tokens(self, tokens):
        assert isinstance(tokens, list)

        tokens = [
            token[0]
            for token in tokens
            if
            token[0] not in self._setStop
            and
            token[1][0] in self._setPos
        ]
        return tokens

    def __removeStopWords(self, question_words):
        assert isinstance(question_words, dict)

        filetred_tokens = {}
        for question, words in question_words.items():
            filetred_tokens[question] = self.__filter_tokens(words)

        return filetred_tokens

    def __repr__(self):
        return str("QuestionAnswerModel")
