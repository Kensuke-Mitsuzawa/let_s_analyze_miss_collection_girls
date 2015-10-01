#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import time

import numpy as np
import os
from chainer import cuda

from models.setting import *
import data_loader
from models import relu_2layer


class ChainerDeepNetWoek(object):
    def __init__(self, model_type, path_input_dir, N, is_add_noise, is_drop, noise_rate):
        assert os.path.exists(path_input_dir)
        assert isinstance(N, int)
        assert isinstance(is_drop, bool)
        assert isinstance(noise_rate, float)

        self.noise_rate = noise_rate
        self.is_drop = is_drop
        self.is_add_noise = is_add_noise

        self.__data_preparation(path_input_dir, N)
        self.__model_selection(model_type)

        self.N = N


    def __model_selection(self, model_type):
        if model_type=='relu_2layer':
            self.forward = relu_2layer.forward
            self.model,self.optimizer = relu_2layer.setup_model(n_dimention=self.n_dimension)

        else:
            raise SystemError()


    def __data_preparation(self, path_input_dir, N):
        assert os.path.exists(path_input_dir)
        assert isinstance(N, int)

        list_of_path = data_loader.make_path_pic_list(path_input_dir)
        dataset = data_loader.make_data_matrix(list_of_input_files=list_of_path)
        train_test_object = data_loader.split_data_train_and_test(dataset, N)

        self.y_train = train_test_object['train']
        self.y_test = train_test_object['test']
        self.N_test = train_test_object['N_test']

        if self.is_add_noise==True:
            self.x_test = self.add_noise(train_set=train_test_object['test'], noise_ratio=self.noise_rate)
            self.x_train = self.add_noise(train_set=train_test_object['train'], noise_ratio=self.noise_rate)
        else:
            self.x_train = train_test_object['train']
            self.x_test = train_test_object['test']
        self.n_dimension = self.x_train.shape[1]



    def add_noise(self, train_set, noise_ratio):
        assert isinstance(train_set, np.ndarray)
        assert isinstance(noise_ratio, float)

        # Add noise
        noised_set = []
        for data in train_set:
            assert isinstance(data, np.ndarray)
            perm = np.random.permutation(data.shape[1])[:int(data.shape[1]*noise_ratio)]
            data[perm] = 0.0
            noised_set.append(data)

        return noised_set


    def train_epoch(self, model, x_train, y_train, optimizer, train_loss):
        # training
        perm = np.random.permutation(self.N)
        sum_loss = 0
        for i in xrange(0, self.N, batchsize):
            x_batch = x_train[perm[i:i+batchsize]]
            y_batch = y_train[perm[i:i+batchsize]]

            optimizer.zero_grads()
            loss = self.forward(model, x_batch, y_batch, self.is_drop)
            loss.backward()
            optimizer.update()

            train_loss.append(loss.data)
            sum_loss += float(cuda.to_cpu(loss.data)) * batchsize

        print '\ttrain mean loss={} '.format(sum_loss / self.N)
        return model, optimizer, train_loss


    def eval_epoch(self, model, epoch, x_test, y_test, start_time,
                   test_mean_loss, test_loss, loss_rate, prev_loss, loss_std, l1_W, l2_W):
        # evaluation
        sum_loss = 0
        for i in xrange(0, self.N_test, batchsize):
            x_batch = x_test[i:i+batchsize]
            y_batch = y_test[i:i+batchsize]
            loss = self.forward(model, x_batch, y_batch, self.is_drop)

            test_loss.append(loss.data)
            sum_loss += float(cuda.to_cpu(loss.data)) * batchsize

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

        for epoch in xrange(1, n_epoch+1):
            print 'epoch', epoch
            start_time = time.clock()
            train_loss = []
            perm = np.random.permutation(self.N)
            sum_loss = 0
            for i in xrange(0, self.N, batchsize):
                x_batch = self.x_train[perm[i:i+batchsize]]
                y_batch = self.y_train[perm[i:i+batchsize]]

                optimizer.zero_grads()
                loss = self.forward(model, x_batch, y_batch, self.is_drop)
                loss.backward()
                optimizer.update()

                train_loss.append(loss.data)
                sum_loss += float(cuda.to_cpu(loss.data)) * batchsize

            print '\ttrain mean loss={} '.format(sum_loss / self.N)

            # evaluation
            sum_loss = 0
            for i in xrange(0, self.N_test, batchsize):
                x_batch = self.x_test[i:i+batchsize]
                y_batch = self.y_test[i:i+batchsize]
                loss = self.forward(model, x_batch, y_batch, self.is_drop)

                test_loss.append(loss.data)
                sum_loss += float(cuda.to_cpu(loss.data)) * batchsize

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

            """
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
                                                                                                    """

        return l1_W, l2_W, test_mean_loss, model



