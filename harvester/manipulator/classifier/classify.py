"""
Deep Learning ----------------------------------------------
"""
# '''Trains and evaluate a simple MLP
# on the Reuters newswire topic classification task.
# '''
# from __future__ import print_function
#
# import numpy as np
# import keras
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation
# from keras.layers import LSTM, Embedding
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from keras.utils import to_categorical
#
# MAX_SEQUENCE_LENGTH = 100  # 每条新闻最大长度
# EMBEDDING_DIM = 200  # 词向量空间维度
# VALIDATION_SPLIT = 0.16  # 验证集比例
# TEST_SPLIT = 0.2  # 测试集比例
#
# NUM_WORDS = 1000
# BATCH_SIZE = 32
# EPOCHS = 5
#
# print('Loading data...')
# # (x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=max_words, test_split=0.2)
# news_texts = []
# label_texts = []
# with open('../dropped_news.txt', 'r') as n:
#     news_texts.extend(list([line.strip('\n') for line in n.readlines()]))
# with open('../dropped_news_label.txt', 'r') as label:
#     label_texts.extend(list([line.strip('\n') for line in label.readlines()]))
#
# print('Vectorizing sequence data...')
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(news_texts)
# sequences = tokenizer.texts_to_sequences(news_texts)
#
# word_index = tokenizer.word_index
# print('Found %s unique tokens.' % len(word_index))
# print('Sequence length: ', len(sequences))
# data = tokenizer.sequences_to_matrix(sequences, mode='tfidf')
# labels = to_categorical(np.asarray(label_texts))
# print('Shape of data tensor:', data.shape)
# print('Shape of label tensor:', labels.shape)
#
#
# p1 = int(len(data)*(1-TEST_SPLIT))
# # p2 = int(len(data)*(1-TEST_SPLIT))
# x_train = data[:p1]
# y_train = labels[:p1]
# # x_val = data[p1:p2]
# # y_val = labels[p1:p2]
# x_test = data[p1:]
# y_test = labels[p1:]
#
# print('x_train shape:', x_train.shape)
# # print('x_val shape:', x_val.shape)
# print('x_test shape:', x_test.shape)
#
# print('\nBuilding model...')
# model = Sequential()
#
# # MLP
# model.add(Dense(512, input_shape=(len(word_index)+1,)))
# model.add(Activation('relu'))
# model.add(Dropout(0.5))
# model.add(Dense(labels.shape[1],))
# model.add(Activation('softmax'))
#
# # # LSTM
# # model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM,
# #           input_length=MAX_SEQUENCE_LENGTH))
# # model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
# # model.add(Dropout(0.2))
# # model.add(Dense(labels.shape[1], activation='softmax'))
#
# model.summary()
#
# print('\nCompiling model...')
# model.compile(loss='categorical_crossentropy',
#               optimizer='adam',
#               metrics=['accuracy'])
#
# print('\nTraining model...')
# history = model.fit(x_train, y_train,
#                     batch_size=BATCH_SIZE,
#                     epochs=EPOCHS,
#                     verbose=1,
#                     validation_split=VALIDATION_SPLIT)
# score = model.evaluate(x_test, y_test,
#                        batch_size=BATCH_SIZE, verbose=1)
# print('Test score:', score[0])
# print('Test accuracy:', score[1])

"""
Machine Learning ----------------------------------------------------
"""

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

MAX_SEQUENCE_LENGTH = 100  # 每条新闻最大长度
VALIDATION_SPLIT = 0.16  # 验证集比例
TEST_SPLIT = 0.2  # 测试集比例

NUM_WORDS = 1000
BATCH_SIZE = 32
EPOCHS = 5

news_texts = []
label_texts = []
print('Loading data...')
with open('../dropped_news.txt', 'r') as n:
    news_texts.extend(list([line.strip('\n') for line in n.readlines()]))
with open('../dropped_news_label.txt', 'r') as label:
    label_texts.extend(list([line.strip('\n') for line in label.readlines()]))

p1 = int(len(news_texts)*(1-TEST_SPLIT))
# p2 = int(len(data)*(1-TEST_SPLIT))
x_train = news_texts[:p1]
y_train = label_texts[:p1]
# x_val = data[p1:p2]
# y_val = labels[p1:p2]
x_test = news_texts[p1:]
y_test = label_texts[p1:]

print('Vectorizing sequence data...')
count_v0 = CountVectorizer()
counts_all = count_v0.fit_transform(news_texts)
count_v1 = CountVectorizer(vocabulary=count_v0.vocabulary_)
counts_train = count_v1.fit_transform(x_train)
print("the shape of train is " + repr(counts_train.shape))
count_v2 = CountVectorizer(vocabulary=count_v0.vocabulary_)
counts_test = count_v2.fit_transform(x_test)
print("the shape of test is " + repr(counts_test.shape))

print('Training...')
tfidftransformer = TfidfTransformer()
train_data = tfidftransformer.fit(counts_train).transform(counts_train)
test_data = tfidftransformer.fit(counts_test).transform(counts_test)


print('Naive Bayes...')
clf = MultinomialNB(alpha=0.01)
clf.fit(train_data, y_train)
pipeline = Pipeline([
    ('vect', count_v0),
    ('tfidf', tfidftransformer),
    ('clf', clf),
])
joblib.dump(pipeline, 'classify_model.pkl')
print(clf.score(test_data, y_test))
'''
About: 0.758
'''

# print('Logistic Regression...')
# lr = LogisticRegression(C=1000)
# lr.fit(train_data, y_train)
# print(lr.score(test_data, y_test))
# '''
# About: 0.746
# '''
#
# print('SVM...')
# svc = SVC(C=1000.0)
# svc.fit(train_data, y_train)
# print(svc.score(test_data, y_test))

