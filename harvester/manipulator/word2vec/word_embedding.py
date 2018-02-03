# coding: utf-8
import numpy as np
import tensorflow as tf


class Word2Vec(object):
    def __init__(self, status):
        self.embedding_size = 200
        self._status = status

        if self._status == 'train':
            self.window_size = 2
        elif self._status == 'predict':
            pass
        else:
            print('')

