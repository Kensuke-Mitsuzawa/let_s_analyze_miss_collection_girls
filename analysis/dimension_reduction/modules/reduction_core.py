#! -*- coding: utf-8 -*-
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.csr import csr_matrix
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
import numpy
import logging

__author__ = 'kensuke-mi'
"""This is core module to called from other script.
"""


def normalize_data(X, norm='l2', axis=1, copy=True):
    assert isinstance(X, numpy.ndarray)
    assert norm in ['l1', 'l2']
    assert axis in [1, 2]
    normalized_X = normalize(X, norm=norm, axis=axis, copy=copy)

    return normalized_X


def call_svd(ndarray_matrix, low_dims, logger, normalize=False):
    assert isinstance(logger, logging.Logger)
    assert isinstance(ndarray_matrix, numpy.ndarray)
    assert isinstance(low_dims, int)

    if normalize == True:
        processed_matrix = normalize_data(ndarray_matrix)
    else:
        processed_matrix = ndarray_matrix

    X = csr_matrix(processed_matrix)
    logger.info(u"original dims: {}".format(X.shape[1]))
    svd = TruncatedSVD(n_components=low_dims, random_state=0)
    X_input = svd.fit_transform(X)
    logger.info(u"after SVD dims: {}".format(X_input.shape[1]))

    return X_input


def call_pca(ndarray_matrix, low_dims, logger, normalize=False):
    assert isinstance(logger, logging.Logger)
    assert isinstance(ndarray_matrix, numpy.ndarray)
    assert isinstance(low_dims, int)

    if normalize == True:
        processed_matrix = normalize_data(ndarray_matrix)
    else:
        processed_matrix = ndarray_matrix

    logger.info(u"original dims: {}".format(processed_matrix.shape[1]))
    pca = PCA(n_components=low_dims)
    X_input = pca.fit_transform(processed_matrix)
    logger.info(u"after PCA dims: {}".format(X_input.shape[1]))

    return X_input


def execute_tsne(ndarray_matrix, target_dims, logger, svd=True, normalize=False):
    assert isinstance(logger, logging.Logger)
    assert isinstance(ndarray_matrix, numpy.ndarray)
    assert isinstance(target_dims, int)
    assert isinstance(normalize, bool)

    if normalize == True:
        processed_matrix = normalize_data(ndarray_matrix)
    else:
        processed_matrix = ndarray_matrix

    if svd==True:
        X_input = call_svd(processed_matrix, 50, logger)
    else:
        if type(processed_matrix) == csr_matrix:
            X_input = processed_matrix.csc_matrix.todense()
        elif type(processed_matrix) == numpy.ndarray:
            X_input = processed_matrix


    model = TSNE(n_components=target_dims, perplexity=40, verbose=2)
    two_dimension_array = model.fit_transform(X_input)

    return two_dimension_array