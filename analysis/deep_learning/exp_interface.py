#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

from train_model import ChainerDeepNetWoek
import matplotlib.pyplot as plt
import math
import models.setting
import os
from numpy import ndarray


def draw_test_mean_loss(test_mean_loss, path_to_graph_png):
    assert isinstance(test_mean_loss, list)
    assert os.path.exists(os.path.dirname(path_to_graph_png))
    # Draw mean loss graph
    plt.style.use('ggplot')
    plt.figure(figsize=(10,7))
    plt.plot(test_mean_loss, lw=1)
    plt.title("")
    plt.ylabel("mean loss")
    plt.show()
    plt.xlabel("epoch")
    plt.savefig(path_to_graph_png)



def draw_digit_w1(size, data, n, i, length):
    assert isinstance(size, int)
    assert isinstance(data, ndarray)
    assert isinstance(n, int)
    assert isinstance(i, int)
    assert isinstance(length, int)

    plt.subplot(math.ceil(length/15), 15, n)
    Z = data.reshape(size,size)   # convert from vector to matrix
    Z = Z[::-1,:]                 # flip vertical
    plt.xlim(0,size)
    plt.ylim(0,size)
    plt.pcolor(Z)
    plt.title("%d"%i, size=9)
    plt.gray()
    plt.tick_params(labelbottom="off")
    plt.tick_params(labelleft="off")


def plot_intermediate_node(l1_W, path_to_plot_png):
    assert os.path.exists(os.path.dirname(path_to_plot_png))
    assert isinstance(l1_W, list)

    array_size = l1_W[-1]
    size = math.sqrt(array_size)

    plt.style.use('fivethirtyeight')
    # draw digit images
    plt.figure(figsize=(15, math.ceil(len(l1_W[models.setting.n_epoch - 1] / 15))))
    cnt = 1

    for i in range(len(l1_W[models.setting.n_epoch - 1])):
        draw_digit_w1(size, l1_W[models.setting.n_epoch - 1][i], cnt, i, len(l1_W[models.setting.n_epoch - 1][i]))
        cnt += 1

    plt.show()
    plt.savefig(path_to_plot_png)


PATH_INPUT_DATA_DIR = '../../extracted/miss_collection/face/gray'
PATH_LOSS_GRAPH_DIR = './graphs/loss_score'
PATH_W1_LAYER_GRAPH_DIR = './graphs/w1_layer'
PATH_W2_LAYER_GRAPH_DIR = './graphs/w2_layer'

def relu_2layer():

    model_type = "relu_2layer"
    relu_2layer_obj = ChainerDeepNetWoek(model_type=model_type,
                                 path_input_dir=PATH_INPUT_DATA_DIR, N=100,
                                 is_add_noise=False, is_drop=False, noise_rate=0.0)
    l1_W, l2_W, test_mean_loss, model = relu_2layer_obj.train_network()
    draw_test_mean_loss(test_mean_loss, path_to_graph_png=os.path.join(PATH_LOSS_GRAPH_DIR, model_type + '.png'))


if __name__ == '__main__':
    relu_2layer()

