'''Trains and evaluate a simple MLP
on the Reuters newswire topic classification task.
'''
from __future__ import print_function

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import LSTM, Embedding
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical

MAX_SEQUENCE_LENGTH = 100  # 每条新闻最大长度
EMBEDDING_DIM = 200  # 词向量空间维度
VALIDATION_SPLIT = 0.16  # 验证集比例
TEST_SPLIT = 0.2  # 测试集比例

NUM_WORDS = 1000
BATCH_SIZE = 32
EPOCHS = 5

print('Loading data...')
# (x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=max_words, test_split=0.2)
news_texts = []
label_texts = []
with open('../news.txt', 'r') as n:
    for line in n.readlines():
        news_texts.append(line.strip('\n'))
with open('../news_label.txt', 'r') as label:
    for line in label.readlines():
        label_texts.append(line.strip('\n'))

print('Vectorizing sequence data...')
tokenizer = Tokenizer(num_words=NUM_WORDS)
tokenizer.fit_on_texts(news_texts)
sequences = tokenizer.texts_to_sequences(news_texts)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
print('Sequence length: ', len(sequences))
data = tokenizer.sequences_to_matrix(sequences, mode='tfidf')
labels = to_categorical(np.asarray(label_texts))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)


p1 = int(len(data)*(1-TEST_SPLIT))
# p2 = int(len(data)*(1-TEST_SPLIT))
x_train = data[:p1]
y_train = labels[:p1]
# x_val = data[p1:p2]
# y_val = labels[p1:p2]
x_test = data[p1:]
y_test = labels[p1:]

print('x_train shape:', x_train.shape)
# print('x_val shape:', x_val.shape)
print('x_test shape:', x_test.shape)

print('\nBuilding model...')
model = Sequential()

# MLP
model.add(Dense(512, input_shape=(NUM_WORDS,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(labels.shape[1],))
model.add(Activation('softmax'))

# # LSTM
# model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM,
#           input_length=MAX_SEQUENCE_LENGTH))
# model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
# model.add(Dropout(0.2))
# model.add(Dense(labels.shape[1], activation='softmax'))

model.summary()

print('\nCompiling model...')
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('\nTraining model...')
history = model.fit(x_train, y_train,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    verbose=1,
                    validation_split=VALIDATION_SPLIT)
score = model.evaluate(x_test, y_test,
                       batch_size=BATCH_SIZE, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])
