import argparse
import pickle
from pylearn2.gui import get_weights_report
from pylearn2.models.dbm.dbm import DBM
from make_dataset_pylearn2 import FacePicDataSet
import numpy
import logging
import os
import draw_graphs
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
logger = logging.getLogger('root_logger')
logger.setLevel(level=logging.INFO)
sh = logging.StreamHandler()
logger.addHandler(sh)

__author__ = 'kensuke-mi'

"""
Visualizes the weight matrices of a pickled model
"""

# This pylearn2 original method returns error. I don't know why.
'''
def show_weights(model_path, rescale="individual",
                 border=False, out=None):
    """
    Show or save weights to an image for a pickled model

    Parameters
    ----------
    model_path : str
        Path of the model to show weights for
    rescale : str
        WRITEME
    border : bool, optional
        WRITEME
    out : str, optional
        Output file to save weights to
    """
    pv = get_weights_report.get_weights_report(model_path=model_path,
                                               rescale=rescale,
                                               border=border)

    if out is None:
        pv.show()
    else:
        pv.save(out)


def make_argument_parser():
    """
    Creates an ArgumentParser to read the options for this script from
    sys.argv
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--rescale", default="individual")
    parser.add_argument("--out", default=None)
    parser.add_argument("--border", action="store_true", default=False)
    parser.add_argument("path")
    return parser
    '''


def draw_hidden_layers(W_T, path_to_plot_png, is_show, logger):
    assert isinstance(W_T, numpy.ndarray)
    assert isinstance(logger, logging.Logger)
    assert os.path.exists(os.path.dirname(path_to_plot_png))
    assert isinstance(is_show, bool)

    logger.info(msg=u"started to draw feature nodes")

    plt.style.use('fivethirtyeight')
    # draw digit images
    array_size = W_T[-1].shape[0]
    size = int(math.sqrt(array_size))

    plt.figure(figsize=(15, math.ceil(len(W_T) / 15)))
    cnt = 1
    COL = 15
    ROW = (W_T.shape[0] / COL) + 1
    for i in range(0, len(W_T)):
        draw_graphs.__draw_digit_w(size=size,
                       data=W_T[i],
                       n=cnt,
                       i=i,
                       col=COL, row=ROW)
        cnt += 1
        logger.info(msg=u'finished drawing {} of {}'.format(i, len(W_T) - 1))

    if is_show==True: plt.show()
    plt.savefig(path_to_plot_png)


def exp_usage():
    path_to_pkl = './model_pylearn2/rbm.pickle/dbm.pkl'
    path_to_plot = './test.png'

    trained_obj = pickle.loads(open(path_to_pkl, 'r').read())
    assert isinstance(trained_obj, DBM)
    # you can get weight with this method
    W = trained_obj.get_weights()
    W_T = W.T
    draw_hidden_layers(W_T=W_T, path_to_plot_png=path_to_plot, is_show=False, logger=logger)


if __name__ == "__main__":
    exp_usage()