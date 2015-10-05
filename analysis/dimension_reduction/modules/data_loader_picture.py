#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'


import os
from PIL import Image
import numpy as np
import pickle


class PictureDataLoader(object):
    def __init__(self, list_path_to_images):
        assert isinstance(list_path_to_images, list)
        self.list_of_input_files = list_path_to_images

    def __convert_into_ndarray(self, path_to_pic, index_no):
        assert os.path.exists(path_to_pic)

        img = np.array( Image.open(path_to_pic), 'f' )
        vector = self.__flatten_image(img)

        return (index_no, path_to_pic, vector)

    def __make_data_mapping_dict(self, list_of_datasource):
        assert isinstance(list_of_datasource, list)
        path_source_mapper = {}
        list_of_array = []
        for data_source_info_tuple in list_of_datasource:
            assert isinstance(data_source_info_tuple, tuple)
            # save data array itself
            list_of_array.append(data_source_info_tuple[2])
            # save index id and its data content
            path_source_mapper[data_source_info_tuple[0]] = data_source_info_tuple[1]

        return path_source_mapper, list_of_array

    def __flatten_image(self, img):
        """
        takes in an (m, n) numpy array and flattens it
        into an array of shape (1, m * n)
        """
        s = img.shape[0] * img.shape[1]
        img_wide = img.reshape(1, s)
        return img_wide[0]

    def make_data_matrix(self, is_convert=True, denominator=255):
        """This method makes list of ndarray from picture data, which represents dataset

        :param list_of_input_files:
        :return:
        """
        assert hasattr(self, "list_of_input_files")
        assert isinstance(self.list_of_input_files, list)
        list_of_datasource = [
            self.__convert_into_ndarray(path_to_pic, index_no=index_no)
            for index_no, path_to_pic
            in enumerate(self.list_of_input_files)
        ]
        path_source_mapper, list_of_array = self.__make_data_mapping_dict(list_of_datasource)

        data_matrix = np.array(list_of_array)
        self.path_index_mapper = path_source_mapper
        if is_convert==True:
            self.data_matrix = data_matrix.astype(np.float32) /denominator
            return path_source_mapper, self.data_matrix
        else:
            self.data_matrix = data_matrix.astype(np.float32)
            return path_source_mapper, self.data_matrix

    def save_into_pickle(self, path_pickle_file):
        assert os.path.exists(os.path.dirname(path_pickle_file))
        file_obj = open(path_pickle_file, 'wb')
        pickle.dump(
            {"data_matrix": self.data_matrix,
             "source_index_mapper": self.path_index_mapper},
            file_obj)
        file_obj.close()
        return path_pickle_file

    def split_data_train_and_test(self, dataset, N):
        assert isinstance(N, int)
        assert isinstance(dataset, np.ndarray)
        assert len(dataset) > N

        train, test = np.split(dataset,   [N])
        N_test = test.shape[0]

        return {"train": train, "test": test, "N_test": N_test}


