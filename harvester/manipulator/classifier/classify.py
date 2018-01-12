# coding: utf-8
"""
TCNNConfig 和 TextCNN 用自https://github.com/gaussic/text-classification-cnn-rnn/blob/master/cnn_model.py
"""
import os
import time
import json
import tensorflow as tf
import tensorflow.contrib.keras as kr
import numpy as np
from django.conf import settings
from dictionary.builder import DictionaryBuilder
from seed.models import Seed
from utils.queryset_iterator import queryset_iterator
from datetime import timedelta

tf.logging.set_verbosity(tf.logging.DEBUG)


class TCNNConfig(object):
    """CNN配置参数"""

    embedding_dim = 64  # 词向量维度
    seq_length = 600  # 序列长度
    num_classes = 10  # 类别数
    num_filters = 256  # 卷积核数目
    kernel_size = 5  # 卷积核尺寸
    vocab_size = 5000  # 词汇表达小

    hidden_dim = 128  # 全连接层神经元

    dropout_keep_prob = 0.5  # dropout保留比例
    learning_rate = 1e-3  # 学习率

    batch_size = 64  # 每批训练大小
    num_epochs = 10  # 总迭代轮次

    print_per_batch = 100  # 每多少轮输出一次结果
    save_per_batch = 10  # 每多少轮存入tensorboard


class TextCNN(object):
    """文本分类，CNN模型"""

    def __init__(self, config):
        self.config = config

        # 三个待输入的数据
        self.input_x = tf.placeholder(tf.int32, [None, self.config.seq_length], name='input_x')
        self.input_y = tf.placeholder(tf.float32, [None, self.config.num_classes], name='input_y')
        self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

        self.cnn()

    def cnn(self):
        """CNN模型"""
        # 词向量映射
        with tf.device('/cpu:0'):
            embedding = tf.get_variable('embedding', [self.config.vocab_size, self.config.embedding_dim])
            embedding_inputs = tf.nn.embedding_lookup(embedding, self.input_x)

        with tf.name_scope("cnn"):
            # CNN layer
            conv = tf.layers.conv1d(embedding_inputs, self.config.num_filters, self.config.kernel_size, name='conv')
            # global max pooling layer
            gmp = tf.reduce_max(conv, reduction_indices=[1], name='gmp')

        with tf.name_scope("score"):
            # 全连接层，后面接dropout以及relu激活
            fc = tf.layers.dense(gmp, self.config.hidden_dim, name='fc1')
            fc = tf.contrib.layers.dropout(fc, self.keep_prob)
            fc = tf.nn.relu(fc)

            # 分类器
            self.logits = tf.layers.dense(fc, self.config.num_classes, name='fc2')
            self.y_pred_cls = tf.argmax(tf.nn.softmax(self.logits), 1)  # 预测类别

        with tf.name_scope("optimize"):
            # 损失函数，交叉熵
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.input_y)
            self.loss = tf.reduce_mean(cross_entropy)
            # 优化器
            self.optim = tf.train.AdamOptimizer(learning_rate=self.config.learning_rate).minimize(self.loss)

        with tf.name_scope("accuracy"):
            # 准确率
            correct_pred = tf.equal(tf.argmax(self.input_y, 1), self.y_pred_cls)
            self.acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32))


class Classifier(object):
    def __init__(self, config):
        self.tcnn = TextCNN(config)
        self.dictionary = self._load_dictionary()

    def _feed_data(self, x_batch, y_batch, keep_prob):
        feed_dict = {
            self.tcnn.input_x: x_batch,
            self.tcnn.input_y: y_batch,
            self.tcnn.keep_prob: keep_prob
        }
        return feed_dict

    def _batch_iter(self, x, y, batch_size=64):
        """生成批次数据"""
        data_len = len(x)
        num_batch = int((data_len - 1) / batch_size) + 1

        indices = np.random.permutation(np.arange(data_len))
        x_shuffle = x[indices]
        y_shuffle = y[indices]

        for i in range(num_batch):
            start_id = i * batch_size
            end_id = min((i + 1) * batch_size, data_len)
            yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]

    def evaluate(self, sess, x_, y_):
        """评估在某一数据上的准确率和损失"""
        data_len = len(x_)
        batch_eval = self._batch_iter(x_, y_, 128)
        total_loss = 0.0
        total_acc = 0.0
        for x_batch, y_batch in batch_eval:
            batch_len = len(x_batch)
            feed_dict = self._feed_data(x_batch, y_batch, 1.0)
            loss, acc = sess.run([self.tcnn.loss, self.tcnn.acc], feed_dict=feed_dict)
            total_loss += loss * batch_len
            total_acc += acc * batch_len

        return total_loss / data_len, total_acc / data_len

    def _load_dictionary(self):
        if not os.path.exists(settings.DICTIONARY):
            db = DictionaryBuilder()
            db.build_dictionary_from_queryset(Seed.objects.filter(usage=1))
        fp = open(settings.DICTIONARY, 'r')
        return json.load(fp)

    def _generate_type_data(self, usage):
        queryset = Seed.objects.filter(usage=usage)
        x_input, y_output = [], []
        for q in queryset_iterator(queryset):
            for w_2_l in q.words['word']:
                x_input.append([self.dictionary[w]
                                for w in w_l for w_l in w_2_l])
                y_output.append(q.content_type)

        x_input = kr.preprocessing.sequence.pad_sequences(
            x_input, self.tcnn.config.seq_length)
        y_output = kr.utils.to_categorical(y_output)

        return x_input, y_output

    def train(self):
        print("Configuring TensorBoard and Saver...")
        # 配置 Tensorboard，重新训练时，请将tensorboard文件夹删除，不然图会覆盖
        tensorboard_dir = settings.TENSORBOARD_PATH
        if not os.path.exists(tensorboard_dir):
            os.makedirs(tensorboard_dir)

        tf.summary.scalar("loss", self.tcnn.loss)
        tf.summary.scalar("accuracy", self.tcnn.acc)
        merged_summary = tf.summary.merge_all()
        writer = tf.summary.FileWriter(tensorboard_dir)

        # 配置 Saver
        saver = tf.train.Saver()
        if not os.path.exists(settings.SESSION_ROOT):
            os.makedirs(settings.SESSION_ROOT)

        print("Loading training and validation data...")
        # 载入训练集与验证集
        start_time = time.time()
        x_train, y_train = self._generate_type_data(usage=1)
        x_val, y_val = self._generate_type_data(usage=2)
        print("Time usage:", timedelta(seconds=int(round(
            time.time() - start_time))))

        # 创建session
        session = tf.Session()
        session.run(tf.global_variables_initializer())
        writer.add_graph(session.graph)

        print('Training and evaluating...')
        total_batch = 0  # 总批次
        best_acc_val = 0.0  # 最佳验证集准确率
        last_improved = 0  # 记录上一次提升批次
        require_improvement = 1000  # 如果超过1000轮未提升，提前结束训练

        flag = False
        for epoch in range(self.tcnn.config.num_epochs):
            print('Epoch:', epoch + 1)
            batch_train = self._batch_iter(x_train, y_train, self.tcnn.config.batch_size)
            for x_batch, y_batch in batch_train:
                feed_dict = self._feed_data(x_batch, y_batch, self.tcnn.config.dropout_keep_prob)

                if total_batch % self.tcnn.config.save_per_batch == 0:
                    # 每多少轮次将训练结果写入tensorboard scalar
                    s = session.run(merged_summary, feed_dict=feed_dict)
                    writer.add_summary(s, total_batch)

                if total_batch % self.tcnn.config.print_per_batch == 0:
                    # 每多少轮次输出在训练集和验证集上的性能
                    feed_dict[self.tcnn.keep_prob] = 1.0
                    loss_train, acc_train = session.run([self.tcnn.loss, self.tcnn.acc], feed_dict=feed_dict)
                    loss_val, acc_val = self.evaluate(session, x_val, y_val)  # todo

                    if acc_val > best_acc_val:
                        # 保存最好结果
                        best_acc_val = acc_val
                        last_improved = total_batch
                        saver.save(sess=session, save_path=settings.SESSION_PATH)
                        improved_str = '*'
                    else:
                        improved_str = ''

                    msg = 'Iter: {0:>6}, Train Loss: {1:>6.2}, Train Acc: {2:>7.2%},' \
                          + ' Val Loss: {3:>6.2}, Val Acc: {4:>7.2%}, Time: {5}'
                    print(msg.format(total_batch, loss_train, acc_train, loss_val, acc_val, improved_str))

                session.run(self.tcnn.optim, feed_dict=feed_dict)  # 运行优化
                total_batch += 1

                if total_batch - last_improved > require_improvement:
                    # 验证集正确率长期不提升，提前结束训练
                    print("No optimization for a long time, auto-stopping...")
                    flag = True
                    break  # 跳出循环
            if flag:  # 同上
                break

    def predict(self):
        pass
