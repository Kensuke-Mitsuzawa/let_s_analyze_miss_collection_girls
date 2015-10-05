#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import time

import numpy as np
import os
import re
import pickle
from chainer import cuda

import data_loader
from models import relu_2layer
from models import sigmoid_2layer


class ChainerDeepNetWoek(object):
    def __init__(self, model_type, path_input_dir, n_units, n_epoch, batchsize, N, is_add_noise, is_drop, noise_rate):
        assert os.path.exists(path_input_dir)
        assert isinstance(N, int)
        assert isinstance(is_drop, bool)
        assert isinstance(noise_rate, float)
        assert isinstance(n_units, int)
        assert isinstance(n_epoch, int)
        assert isinstance(batchsize, int)

        self.n_unit = n_units
        self.n_epoch = n_epoch
        self.batchsize = batchsize

        self.noise_rate = noise_rate
        self.is_drop = is_drop
        self.is_add_noise = is_add_noise

        self.__data_preparation(path_input_dir, N)
        self.__model_selection(model_type)

        self.N = N


    def __model_selection(self, model_type):
        """This method load model structure from other script file. You can add new modes if you add some rules

        :param model_type:
        :return:
        """
        if re.findall(r'relu_2layer', model_type)!=[]:
            self.forward = relu_2layer.forward
            self.model,self.optimizer = relu_2layer.setup_model(n_dimention=self.n_dimension, n_units=self.n_unit)

        elif re.findall(r'sigmoid_2layer', model_type)!=[]:
            self.forward = sigmoid_2layer.forward
            self.model,self.optimizer = sigmoid_2layer.setup_model(n_dimention=self.n_dimension, n_units=self.n_unit)

        else:
            raise SystemError()


    def __data_preparation(self, path_input_dir, N):
        assert os.path.exists(path_input_dir)
        assert isinstance(N, int)

        list_of_path = data_loader.make_path_pic_list(path_input_dir)
        index_datapath_mapper, dataset = data_loader.make_data_matrix(list_of_input_files=list_of_path)
        self.dataset = dataset
        self.index_datapath_mapper = index_datapath_mapper
        train_test_object = data_loader.split_data_train_and_test(self.dataset, N)

        self.y_train = train_test_object['train']
        self.y_test = train_test_object['test']
        self.N_test = train_test_object['N_test']

        if self.is_add_noise==True:
            x_train = self.add_noise(train_set=train_test_object['train'], noise_ratio=self.noise_rate)
            x_test = self.add_noise(train_set=train_test_object['test'], noise_ratio=self.noise_rate)
            n_dimension = x_train.shape[1]
        else:
            x_train = train_test_object['train']
            x_test = train_test_object['test']
            n_dimension = x_train.shape[1]

        assert isinstance(x_train, np.ndarray)
        assert isinstance(x_test, np.ndarray)
        assert len(x_train.shape) == 2
        assert len(x_test.shape) == 2

        self.x_train = x_train
        self.x_test = x_test
        self.n_dimension = n_dimension

    def add_noise(self, train_set, noise_ratio):
        assert isinstance(train_set, np.ndarray)
        assert isinstance(noise_ratio, float)

        # Add noise
        noised_set = []
        for data in train_set:
            assert isinstance(data, np.ndarray)
            perm = np.random.permutation(data.shape[0])[:int(data.shape[0]*noise_ratio)]
            data[perm] = 0.0
            noised_set.append(data)

        return np.array(noised_set)


    def train_epoch(self, model, x_train, y_train, optimizer, train_loss):
        # training
        perm = np.random.permutation(self.N)
        sum_loss = 0
        for i in xrange(0, self.N, self.batchsize):
            x_batch = x_train[perm[i:i+self.batchsize]]
            y_batch = y_train[perm[i:i+self.batchsize]]

            optimizer.zero_grads()
            loss = self.forward(model, x_batch, y_batch, self.is_drop)
            loss.backward()
            optimizer.update()

            train_loss.append(loss.data)
            sum_loss += float(cuda.to_cpu(loss.data)) * self.batchsize

        print '\ttrain mean loss={} '.format(sum_loss / self.N)
        return model, optimizer, train_loss


    def eval_epoch(self, model, epoch, x_test, y_test, start_time,
                   test_mean_loss, test_loss, loss_rate, prev_loss, loss_std, l1_W, l2_W):
        # evaluation
        sum_loss = 0
        for i in xrange(0, self.N_test, self.batchsize):
            x_batch = x_test[i:i+self.batchsize]
            y_batch = y_test[i:i+self.batchsize]
            loss = self.forward(model, x_batch, y_batch, self.is_drop)

            test_loss.append(loss.data)
            sum_loss += float(cuda.to_cpu(loss.data)) * self.batchsize

        loss_val = sum_loss / self.N_test

        print '\ttest  mean loss={}'.format(loss_val)
        if epoch == 1:
            loss_std = loss_val
            loss_rate.append(100)
        else:
            print '\tratio :%.3f'%(loss_val/loss_std * 100)
            loss_rate.append(loss_val/loss_std * 100)

        if prev_loss >= 0:
            diff = loss_val - prev_loss
            ratio = diff/prev_loss * 100
            print '\timpr rate:%.3f'%(-ratio)

        prev_loss = sum_loss / self.N_test
        test_mean_loss.append(loss_val)

        # TODO これ実はこのモデルだけに使える話だから考えないと
        l1_W.append(model.l1.W)
        l2_W.append(model.l2.W)
        end_time = time.clock()
        print "\ttime = %.3f" %(end_time - start_time)

        return prev_loss, loss_std, loss_rate, test_loss, test_mean_loss, l1_W, l2_W


    def train_network(self):
        # Learning loop
        l1_W = []
        l2_W = []

        test_loss = []
        test_mean_loss = []

        prev_loss = -1
        loss_std = 0
        loss_rate = []

        model = self.model
        optimizer = self.optimizer


        for epoch in xrange(1, self.n_epoch+1):
            print 'epoch', epoch
            start_time = time.clock()
            train_loss = []

            model, optimizer, train_loss = self.train_epoch(model=model,
                                                            x_train=self.x_train,
                                                            y_train=self.y_train,
                                                            optimizer=optimizer,
                                                            train_loss=train_loss)

            prev_loss, loss_std, loss_rate, test_loss, test_mean_loss, l1_W, l2_W = self.eval_epoch(model=model,
                                                                                                    epoch=epoch,
                                                                                                    x_test=self.x_test,
                                                                                                    y_test=self.y_test,
                                                                                                    start_time=start_time,
                                                                                                    test_mean_loss=test_mean_loss,
                                                                                                    test_loss=test_loss,
                                                                                                    loss_rate=loss_rate,
                                                                                                    prev_loss=prev_loss,
                                                                                                    loss_std=loss_std,
                                                                                                    l1_W=l1_W,
                                                                                                    l2_W=l2_W)

        self.l1_W = l1_W
        self.l2_W = l2_W
        self.model = model
        self.test_mean_loss = test_mean_loss

        return l1_W, l2_W, test_mean_loss, model



    def save_trained_models(self, path_to_pickle):
        assert hasattr(self, "l1_W")
        assert hasattr(self, "l2_W")
        assert hasattr(self, "model")
        assert hasattr(self, "test_mean_loss")
        assert hasattr(self, "dataset")
        assert os.path.exists(os.path.dirname(path_to_pickle))

        save_obj = {}
        save_obj["l1_W"] = self.l1_W
        save_obj["l2_W"] = self.l2_W
        save_obj["model"] = self.model
        save_obj["test_mean_loss"] = self.test_mean_loss
        save_obj['dataset'] = self.dataset
        save_obj['index_datapath_mapper'] = self.index_datapath_mapper

        f = open(path_to_pickle, "w")
        pickle.dump(save_obj, f)
        f.close()





