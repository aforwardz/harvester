# coding: utf-8
from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Bidirectional
from keras.layers import Dense
from keras.layers import TimeDistributed
from keras.layers import Dropout
from keras_contrib.layers.crf import CRF
from keras_contrib.utils import save_load_utils

VOCAB_SIZE = 2500
EMBEDDING_OUT_DIM = 128
TIME_STAMPS = 100
HIDDEN_UNITS = 200
DROPOUT_RATE = 0.3
NUM_CLASS = 5


def build_embedding_bilstm2_crf_model():
    """
    带embedding的双向LSTM + crf
    """
    model = Sequential()
    model.add(Embedding(VOCAB_SIZE, output_dim=EMBEDDING_OUT_DIM, input_length=TIME_STAMPS))
    model.add(Bidirectional(LSTM(HIDDEN_UNITS, return_sequences=True)))
    model.add(Dropout(DROPOUT_RATE))
    model.add(Bidirectional(LSTM(HIDDEN_UNITS, return_sequences=True)))
    model.add(Dropout(DROPOUT_RATE))
    model.add(TimeDistributed(Dense(NUM_CLASS)))
    crf_layer = CRF(NUM_CLASS)
    model.add(crf_layer)
    model.compile('rmsprop', loss=crf_layer.loss_function, metrics=[crf_layer.accuracy])
    return model


def save_embedding_bilstm2_crf_model(model, filename):
    save_load_utils.save_all_weights(model, filename)


def load_embedding_bilstm2_crf_model(filename):
    model = build_embedding_bilstm2_crf_model()
    save_load_utils.load_all_weights(model, filename)
    return model


if __name__ == '__main__':
    model = build_embedding_bilstm2_crf_model()
