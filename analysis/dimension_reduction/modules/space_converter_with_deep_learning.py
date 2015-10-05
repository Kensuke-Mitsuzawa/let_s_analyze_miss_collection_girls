#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
import pickle
import os
import numpy


class SpaceConverterDeepFeature(object):
    def __init__(self, path_to_trained_model_pickle):
        assert os.path.exists(path_to_trained_model_pickle)

        model_object = self.__load_pickle_obj(path_to_trained_model_pickle)
        assert isinstance(model_object, dict)
        self.feature_vector = model_object['l1_W'][-1]
        self.data_matrix = model_object['dataset']

    def __load_pickle_obj(self, path_to_trained_model_pickle):
        file_obj = open(path_to_trained_model_pickle, 'rb')
        model_object = pickle.load(file_obj)
        assert isinstance(model_object, dict)

        return model_object

    def select_feature_vectors(self, vector_index_numbers):
        assert isinstance(vector_index_numbers, list)
        selected_vectors = []
        for vector_index in vector_index_numbers:
            vector = self.feature_vector[vector_index]
            selected_vectors.append(vector)

        return numpy.array(selected_vectors)

    def space_convert(self, feature_vectors):
        assert hasattr(self, "data_matrix")
        assert isinstance(feature_vectors, numpy.ndarray)
        assert isinstance(self.data_matrix, numpy.ndarray)

        new_space_matrix = numpy.dot(a=self.data_matrix, b=feature_vectors.T)
        return new_space_matrix