import numpy
from pylearn2.datasets import DenseDesignMatrix
from pylearn2.utils import serial
import data_loader
import os
"""This script makes dataset for pylearn2
"""
__author__ = 'kensuke-mi'


class FacePicDataSet(DenseDesignMatrix):
    def __init__(self, data):
        self.data = data
        super(FacePicDataSet, self).__init__(X=data) #, y=self.y)


def main(list_of_input_files, path_to_save_directory, project_name):
    assert isinstance(list_of_input_files, list)
    assert os.path.exists(path_to_save_directory)
    assert isinstance(project_name, (str, unicode))

    if os.path.exists(os.path.join(path_to_save_directory, project_name))==False:
        os.mkdir(os.path.join(path_to_save_directory, project_name))

    source_index_mapper, data_matrix = data_loader.make_data_matrix(list_of_input_files=list_of_input_files)

    train = FacePicDataSet(data=data_matrix)
    train.use_design_loc(os.path.join(path_to_save_directory, project_name, '{}.npy'.format(project_name)))

    train_csv_path = os.path.join(path_to_save_directory, project_name, '{}.csv'.format(project_name))
    train_pkl_path = os.path.join(path_to_save_directory, project_name, '{}.pkl'.format(project_name))
    # save in csv
    numpy.savetxt(train_csv_path, data_matrix, delimiter=',', fmt='%s')
    # save in pickle
    serial.save(train_pkl_path, train)


def exp_interface():
    """make dataset for pylearn2 from girls' face gray scaled pictures
    :return:
    """
    path_index_path = '../../extracted/miss_collection/gray'
    input_files_list = data_loader.make_path_pic_list(path_input_dir=path_index_path)

    path_to_save_directory = 'intermediate_files_pylearn2'
    project_name = 'toy_train'
    main(input_files_list, path_to_save_directory, project_name)

if __name__ == '__main__':
    exp_interface()