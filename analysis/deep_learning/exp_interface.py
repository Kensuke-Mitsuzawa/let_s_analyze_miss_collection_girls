#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

from train_model import ChainerDeepNetWoek
import matplotlib.pyplot as plt
import math
import os
from numpy import ndarray


def draw_test_mean_loss(test_mean_loss, path_to_graph_png, is_show=False):
    assert isinstance(test_mean_loss, list)
    assert os.path.exists(os.path.dirname(path_to_graph_png))
    # Draw mean loss graph
    plt.style.use('ggplot')
    plt.figure(figsize=(10,7))
    plt.plot(test_mean_loss, lw=1)
    plt.title("")
    plt.ylabel("mean loss")
    if is_show==True: plt.show()
    plt.xlabel("epoch")
    plt.savefig(path_to_graph_png)


def __draw_digit_w(size, data, n, row, col, i, length):
    assert isinstance(size, int)
    assert isinstance(data, ndarray)
    assert isinstance(n, int)
    assert isinstance(i, int)
    assert isinstance(length, int)

    plt.subplot(row, col, n)
    Z = data.reshape(size, size)   # convert from vector to matrix
    Z = Z[::-1,:]                 # flip vertical
    plt.xlim(0, size)
    plt.ylim(0, size)
    plt.pcolor(Z)

    plt.title("%d"%i, size=8)
    plt.gray()
    plt.tick_params(labelbottom="off")
    plt.tick_params(labelleft="off")


def plot_intermediate_node(l1_W, path_to_plot_png, n_epoch, is_show=False):
    assert os.path.exists(os.path.dirname(path_to_plot_png))
    assert isinstance(l1_W, list)
    assert isinstance(n_epoch, int)

    array_size = l1_W[-1].shape[1]
    size = int(math.sqrt(array_size))

    plt.style.use('fivethirtyeight')
    # draw digit images
    plt.figure(figsize=(15, math.ceil(len(l1_W[n_epoch - 1]) / 15)))
    cnt = 1
    COL=15
    ROW=(l1_W[n_epoch - 1].shape[0] / COL) + 1
    for i in range(0, len(l1_W[n_epoch - 1])):
        __draw_digit_w(size=size,
                       data=l1_W[n_epoch - 1][i],
                       n=cnt,
                       i=i,
                       length=len(l1_W[n_epoch - 1][i]),
                       col=COL, row=ROW)
        cnt += 1

    if is_show==True: plt.show()
    plt.savefig(path_to_plot_png)


# draw a image of handwriting number
def draw_digit_ae(size, data, n, row, col, _type):
    plt.subplot(row, col, n)
    Z = data.reshape(size,size)
    Z = Z[::-1,:]                 # flip vertical
    plt.xlim(0,150)
    plt.ylim(0,150)
    plt.pcolor(Z)
    plt.title("type=%s"%(_type), size=8)
    plt.gray()
    plt.tick_params(labelbottom="off")
    plt.tick_params(labelleft="off")



PATH_INPUT_DATA_DIR = '../../extracted/miss_collection/face/gray'
PATH_LOSS_GRAPH_DIR = './graphs/loss_score'
PATH_W1_LAYER_GRAPH_DIR = './graphs/w1_layer'
PATH_W2_LAYER_GRAPH_DIR = './graphs/w2_layer'

def relu_2layer():
    N_UNIT = 1000
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 100

    model_type = "relu_2layer_drop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=True, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'))


def relu_2layer_nodrop():
    N_UNIT = 1000
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 100

    model_type = "relu_2layer_nodrop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=False, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'))



def relu_2layer_400_unit_drop():
    N_UNIT = 400
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 100

    model_type = "relu_2layer_400_layer_drop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=True, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'))



def relu_2layer_400_unit_nodrop():
    N_UNIT = 400
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 100

    model_type = "relu_2layer_400_layer_nodrop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=False, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'))



def sigmoid_2layer_drop():
    N_UNIT = 1000
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 100

    model_type = "sigmoid_2layer_drop"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=False, is_drop=True, noise_rate=0.0,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'))


def sigmoid_2layer_drop_noise():
    N_UNIT = 1000
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 100

    model_type = "sigmoid_2layer_drop_noise"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=True, is_drop=True, noise_rate=0.2,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'))


def sigmoid_2layer_100_nodrop_noise():
    N_UNIT = 100
    N_EPOCH = 30
    BATCHSIZE = 100
    N = 100

    model_type = "sigmoid_2layer_100_nodrop_noise"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=N,
                                 is_add_noise=True, is_drop=False, noise_rate=0.2,
                                 n_units=N_UNIT, n_epoch=N_EPOCH, batchsize=BATCHSIZE)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


    plot_intermediate_node(l1_W=l1_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W1_LAYER_GRAPH_DIR, model_type + '.png'))
    plot_intermediate_node(l1_W=l2_W, n_epoch=N_EPOCH,
                           path_to_plot_png=os.path.join(PATH_W2_LAYER_GRAPH_DIR, model_type + '.png'))


if __name__ == '__main__':
    relu_2layer()

