#! -*- coding: utf-8 -*-
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.csr import csr_matrix
from sklearn.manifold import TSNE
import numpy
import logging

__author__ = 'kensuke-mi'
"""This is core module to called from other script.
"""

# TODO 正規化を実施すること。標準偏差と平均で正規化すれば、十分なはず

def call_svd(ndarray_matrix, low_dims, logger):
    assert isinstance(logger, logging.Logger)
    assert isinstance(ndarray_matrix, numpy.ndarray)
    assert isinstance(low_dims, int)

    X = csr_matrix(ndarray_matrix)
    logger.info(u"original dims: {}".format(X.shape[1]))
    svd = TruncatedSVD(n_components=low_dims, random_state=0)
    X_input = svd.fit_transform(X)
    logger.info(u"after SVD dims: {}".format(X_input.shape[1]))

    return X_input


def execute_tsne(ndarray_matrix, target_dims, logger, svd=True):
    assert isinstance(logger, logging.Logger)
    assert isinstance(ndarray_matrix, numpy.ndarray)
    assert isinstance(target_dims, int)

    if svd==True:
        X_input = call_svd(ndarray_matrix, 50, logger)
    else:
        X_input = ndarray_matrix.csc_matrix.todense()


    model = TSNE(n_components=target_dims, perplexity=40, verbose=2)
    two_dimension_array = model.fit_transform(X_input)

    return two_dimension_array