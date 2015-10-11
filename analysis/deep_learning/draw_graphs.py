#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
import os
from numpy import ndarray
import numpy
import matplotlib
# if you're using ubuntu
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import logging


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


def __draw_digit_w(size, data, n, row, col, i):
    assert isinstance(size, int)
    assert isinstance(n, int)
    assert isinstance(i, int)

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


def plot_intermediate_node(l1_W, path_to_plot_png, n_epoch, datatype, logger, is_show=False):
    assert os.path.exists(os.path.dirname(path_to_plot_png))
    assert isinstance(l1_W, list)
    assert isinstance(n_epoch, int)
    assert isinstance(logger, logging.Logger)

    logger.info(msg=u"started to draw feature nodes")

    plt.style.use('fivethirtyeight')
    # draw digit images
    if datatype=='vector':
        array_size = l1_W[-1].shape[1]
        size = int(math.sqrt(array_size))

        plt.figure(figsize=(15, math.ceil(len(l1_W[n_epoch - 1]) / 15)))
        cnt = 1
        COL=15
        ROW=(l1_W[n_epoch - 1].shape[0] / COL) + 1
        for i in range(0, len(l1_W[n_epoch - 1])):
            __draw_digit_w(size=size,
                           data=l1_W[n_epoch - 1][i],
                           n=cnt,
                           i=i,
                           col=COL, row=ROW)
            cnt += 1
            logger.info(msg=u'finished drawing {} of {}'.format(i, len(l1_W[n_epoch - 1]) - 1))

    elif datatype=='matrix':
        # 画像サイズを設定する
        array_size = l1_W[-1].shape[0]
        size = int(math.sqrt(array_size))

        aaa = len(l1_W[n_epoch - 1]) / 15
        fig_size_height = math.ceil(len(l1_W[n_epoch - 1]) / 15)
        fig_size_width = 15
        plt.figure(figsize=(15, 100))
        cnt = 1
        COL = 15
        ROW = (l1_W[n_epoch - 1].shape[1] / COL) + 1
        W_T = numpy.array(l1_W[n_epoch - 1]).T
        for i in range(0, W_T.shape[0]):
            __draw_digit_w(size=size,
                           data=W_T[i],
                           n=cnt,
                           i=i+1,
                           col=COL, row=ROW)
            logger.info(msg=u'finished drawing {} of {}'.format(i, W_T.shape[0] - 1))
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
