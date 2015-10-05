#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

from train_model import ChainerDeepNetWoek
from draw_graphs import *
import os
import logging
logger = logging.getLogger('root_logger')
logger.setLevel(level=logging.INFO)
sh = logging.StreamHandler()
logger.addHandler(sh)


PATH_INPUT_DATA_DIR = '../../extracted/miss_collection/gray'
PATH_LOSS_GRAPH_DIR = './graphs/loss_score'
PATH_W1_LAYER_GRAPH_DIR = './graphs/w1_layer'
PATH_W2_LAYER_GRAPH_DIR = './graphs/w2_layer'
PATH_TRAINED_MODELS = './trained_models'

# -----------------------------------------------------------------------
def __make_model_pickle_path(path_trained_model_dir, model_name):
    return os.path.join(path_trained_model_dir, '{}.pickle'.format(model_name))


def simple_test():
    N_UNIT = 100
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 400

    model_type = "relu_2layer_simple_test"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=True, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'),
                           logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           datatype='matrix',
                           logger=logger)


def relu_2layer():
    N_UNIT = 1000 
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 400

    model_type = "relu_2layer_drop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=True, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()

    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'),
                           logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH, datatype='matrix',
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           logger=logger)


def relu_2layer_nodrop():
    N_UNIT = 1000
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 110

    model_type = "relu_2layer_nodrop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=False, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))


    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'),
                           logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           datatype="matrix",
                           logger=logger)



def relu_2layer_400_unit_drop():
    N_UNIT = 400
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 400

    model_type = "relu_2layer_400_layer_drop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=True, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))

    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'),
                           logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           datatype='matrix', logger=logger)



def relu_2layer_400_unit_nodrop():
    N_UNIT = 400
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 110

    model_type = "relu_2layer_400_layer_nodrop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=False, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))

    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'), logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           datatype='matrix', logger=logger)



def sigmoid_2layer_drop():
    N_UNIT = 1000
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 110

    model_type = "sigmoid_2layer_drop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=True, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'), logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           logger=logger)


def sigmoid_2layer_drop_noise():
    N_UNIT = 1000
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 110

    model_type = "sigmoid_2layer_drop_noise"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=True, is_drop=True, noise_rate=0.2,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'),
                           logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           datatype='matrix', logger=logger)


def sigmoid_2layer_100_nodrop_noise():
    N_UNIT = 100
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 110

    model_type = "sigmoid_2layer_100_nodrop_noise"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=True, is_drop=False, noise_rate=0.2,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    relu_2layer_obj.save_trained_models(__make_model_pickle_path(PATH_TRAINED_MODELS, model_type))

    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH, datatype='vector',
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'), logger=logger)
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'),
                           datatype='matrix', logger=logger)


if __name__ == '__main__':
    import resource
    rsrc = resource.RLIMIT_DATA
    soft, hard = resource.getrlimit(rsrc)
    print 'Soft limit starts as  :', soft
    resource.setrlimit(rsrc, (1024, hard)) #limit to one kilobyte
    soft, hard = resource.getrlimit(rsrc)
    print 'Soft limit changed to :', soft
    
    #simple_test()
    #relu_2layer()
    #relu_2layer_nodrop()
    #relu_2layer_400_unit_drop()
    #relu_2layer_400_unit_nodrop()
    sigmoid_2layer_100_nodrop_noise()
    sigmoid_2layer_drop()
    sigmoid_2layer_drop_noise()
