#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'


from sklearn.decomposition import TruncatedSVD
from scipy.sparse.csr import csr_matrix
from sklearn.manifold import TSNE
import logging


def call_svd(texts_obj, low_dims, logger):
    assert isinstance(logger, logging.Logger)

    X = csr_matrix(texts_obj.csc_matrix)
    logger.info(u"original dims: {}".format(X.shape[1]))
    svd = TruncatedSVD(n_components=low_dims, random_state=0)
    X_input = svd.fit_transform(X)
    logger.info(u"after SVD dims: {}".format(X_input.shape[1]))

    return X_input


def execute_tsne(texts_obj, target_dims, logger, svd=True):
    assert isinstance(logger, logging.Logger)

    if svd==True:
        X_input = call_svd(texts_obj, 50, logger)
    else:
        X_input = texts_obj.csc_matrix.todense()


    model = TSNE(n_components=target_dims, perplexity=40, verbose=2)
    two_dimension_array = model.fit_transform(X_input)

    return two_dimension_array