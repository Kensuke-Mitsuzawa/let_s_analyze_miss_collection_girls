import os
# --------------------------------------
from pylearn2.testing import skip
from pylearn2.testing import no_debug_mode
from pylearn2.config import yaml_parse
# --------------------------------------
from make_dataset_pylearn2 import FacePicDataSet

"""This script execute training based on pylearn2.
Basically, this script requires *yaml file in which training method is described and
pickle file in which training data is.
"""

__author__ = 'kensuke-mi'

PATH_TO_PYLEARN2_MODES_DIR = os.path.abspath('./model_pylearn2')


@no_debug_mode
def train_yaml(yaml_file):

    train = yaml_parse.load(yaml_file)
    train.main_loop()


def train_grdm_dbm_mode(yaml_models_dir):
    input_pickle_path = os.path.abspath('./model_pylearn2/toy_train.pkl')
    yaml_file_path = os.path.join(yaml_models_dir, 'grdm_dbm.yaml')
    save_path = os.path.join(yaml_models_dir, 'grdm_dbm.pickle')
    yaml = open(yaml_file_path, 'r').read()

    print input_pickle_path
    hyper_params = {'batch_size': 100,
                    'nvis': 200,
                    'detector_layer_dim1': 300,
                    'detector_layer_dim2': 300,
                    'detector_layer_dim3': 10,
                    'monitoring_batches': 10,
                    'max_epochs': 100,
                    'save_path': save_path,
                    'input_pickle_path': input_pickle_path}

    yaml = yaml % (hyper_params)
    train_yaml(yaml)


def train_dbm_model(yaml_models_dir):

    input_pickle_path = os.path.abspath('./model_pylearn2/toy_train.pkl')
    yaml_file_path = os.path.join(yaml_models_dir, 'rbm.yaml')
    save_path = os.path.join(yaml_models_dir, 'rbm.pickle')

    yaml = open(yaml_file_path, 'r').read()

    hyper_params = {'detector_layer_dim': 500,
                    'monitoring_batches': 10,
                    'train_stop': 50000,
                    'max_epochs': 300,
                    'save_path': save_path,
                    'input_pickle_path': input_pickle_path}

    yaml = yaml % (hyper_params)
    train_yaml(yaml)


def train_generic():

    skip.skip_if_no_data()
    train_dbm_model(PATH_TO_PYLEARN2_MODES_DIR)


if __name__ == '__main__':
    train_generic()