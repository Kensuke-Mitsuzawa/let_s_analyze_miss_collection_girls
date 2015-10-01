#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
import numpy as np
from chainer import Variable
import chainer.functions as F
from chainer import FunctionSet
from chainer import optimizers
from setting import *



def forward(model, x_data, y_data, is_drop):
    assert isinstance(is_drop, bool)
    assert isinstance(x_data, np.ndarray)
    assert isinstance(y_data, np.ndarray)

    x, t = Variable(x_data), Variable(y_data)
    y = F.dropout(F.relu(model.l1(x)),  train=is_drop)
    x_hat  = F.dropout(model.l2(y),  train=is_drop)
    # 誤差関数として二乗誤差関数を用いる
    return F.mean_squared_error(x_hat, t)


def setup_model(n_dimention):

    model = FunctionSet(l1=F.Linear(n_dimention, n_units),
                        l2=F.Linear(n_units, n_dimention))
    # Setup optimizer
    optimizer = optimizers.Adam()
    optimizer.setup(model.collect_parameters())

    return model, optimizer


