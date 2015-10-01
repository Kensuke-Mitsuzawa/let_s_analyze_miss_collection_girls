#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import unittest
from analysis.deep_learning.data_loader import *
from numpy import ndarray
from sklearn.datasets import fetch_mldata


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.path_input_dir = './pics'
        print 'fetch MNIST dataset'
        self.mnist = fetch_mldata('MNIST original')


    def test_make_path_pic_list(self):
        path_to_files = make_path_pic_list(self.path_input_dir)
        assert len(path_to_files) == 2

        return path_to_files

    def test_make_data_matrix(self):
        path_to_files = self.test_make_path_pic_list()
        list_of_ndarray = make_data_matrix(path_to_files)
        assert isinstance(list_of_ndarray, ndarray)
        for dataset in list_of_ndarray: assert isinstance(dataset, ndarray)




def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDataLoader)

    return suite