import os
import multiprocessing
import tensorflow as tf

from multiprocessing import queues
from manipulator import settings
from django.db import models
from utils.queryset_iterator import queryset_iterator

import logging

logger = logging.getLogger('tfrecord')


class ObjectProducer(object):
    """ 基于 queryset 的 Producer, 消耗常量内存
    NOTE: 这里的 queue 必须是 multiprocessing.Queue
    """

    def __init__(self, _queue, maxsize=2000):
        self._maxsize = maxsize
        if not isinstance(_queue, queues.Queue):
            raise TypeError('queue must be instance of multiprocessing.Queue!')
        self.queue = _queue
        self._producers = list()

    def obj_producer(self, queryset):
        logger.info('PID: {pid} ObjectProducer start producing,\
                Queue size: {queue_size}'.format(
            pid=os.getpid(),
            queue_size=self._maxsize
        ))
        count = 0
        if isinstance(queryset, (list, tuple, set)):
            for obj in queryset:
                self.queue.put(obj)
                count += 1
        elif isinstance(queryset, models.QuerySet):
            for obj in queryset_iterator(
                    queryset=queryset, chunksize=self._maxsize):
                self.queue.put(obj)
                count += 1
        else:
            raise TypeError('Unexpected queryset')

        logger.info('PID: %d ObjectProducer finish produce, count: %d' % (os.getpid(), count))

    def start_producing(self, queryset):
        """ 这里当前只需要一个 process 就够了
        如果要考虑多个 producer，需要对 queryset 处理
        """
        producer = multiprocessing.Process(
            target=self.obj_producer, args=(queryset,)
        )
        producer.start()
        self._producers.append(producer)

    def join(self):
        """ 阻塞主进程"""
        for producer in self._producers:
            producer.join()


class TFRecordWriter(object):
    """ worker queue.get() -> worker write tfrecord
    """

    def __init__(self, _queue, writer_cls=None):
        self._writer_cls = writer_cls if writer_cls \
            else tf.python_io.TFRecordWriter
        self.queue = _queue
        self._writers = list()  # multiprocessing.Queue()

    def _tfrecord_writer_gen(self, basename, filename, worker_num=1):
        """
        :param basename: basedir name
        :param filename: file prefix name
        :param worker_num: workers number
        :return: writers based on workers
        """
        for i in range(worker_num):
            filepath = self._get_filepath(basename, filename, str(i))
            yield self._writer_cls(filepath), filepath

    def _write(self, features_gen, writer):
        """ For best performance:
        https://github.com/tensorflow/tensorflow/blob/master/tensorflow
        /docs_src/install/install_linux.md#protobuf-pip-package-31
        :type features_gen: generator
        :param writer: tf.python_io.TFRecordWriter
        """
        for feature in features_gen:
            example = tf.train.Example(
                features=tf.train.Features(feature=feature)
            )
            writer.write(record=example.SerializeToString())

    def get_feature_example(self, feature):
        example = tf.train.Example(
            features=tf.train.Features(feature=feature)
        )
        return example

    def writer(self, _writer, filepath, feature_name_list, timeout=10):
        """ NOTE:
            这里的应用场景是，``producer`` 明显产出更快（虽然当前只有一个process），
            一般情况下，``queue`` 里空了，便认为是被所有消费者消费了。
            故这里，在一定 ``timeout`` 下，如果没有东西了，消费者便自动销毁。
        """
        count = 0
        logger.info('PID: %d Writer starting...' % (os.getpid(),))
        while 1:
            try:
                obj = self.queue.get(timeout=timeout)
            except:
                _writer.close()
                break
            else:
                if not hasattr(obj, 'feature_gen'):
                    raise AttributeError('Object %s has no attrbute feature_gen' % repr(obj))

                # 在不同的class上，有方法的依赖不是很好
                for feature in obj.feature_gen(feature_name_list):
                    if not feature:
                        continue
                    example = self.get_feature_example(feature)
                    _writer.write(record=example.SerializeToString())
                count += 1
        base, ext = os.path.splitext(filepath)
        new_path = base + str(count) + ext
        os.rename(filepath, new_path)
        logger.info('PID: %d Writer closed, count: %d \n    -> File saved: %s'
                    % (os.getpid(), count, new_path))

    def start_consuming(
            self,
            basename,
            feature_name_list,
            filename='material',
            worker_num=None
    ):
        worker_num = self._get_worker_num(worker_num)
        for _writer, filepath in self._tfrecord_writer_gen(basename, filename, worker_num):
            writer = multiprocessing.Process(
                target=self.writer, args=(_writer, filepath, feature_name_list,))
            writer.start()
            self._writers.append(writer)

    def join(self):
        """阻塞主进程"""
        for writer in self._writers:
            writer.join()

    def _get_worker_num(self, worker_num=None):
        """ For best practice:
        https://stackoverflow.com/questions/20039659/python-multiprocessings
        -pool-process-limit
        :param worker_num:
        :return:
        """
        worker_num = worker_num or multiprocessing.cpu_count()
        return worker_num

    def _get_filepath(self, basename, filename, suffix='pid0', ext='tfrecord'):
        base_directory = os.path.join(settings.TFRECORD_ROOT, basename)
        if not os.path.exists(base_directory):
            os.makedirs(base_directory)

        # P: Pid; C: Count
        filename = '{}_P{}_C.{}'.format(filename, suffix, ext)
        return os.path.join(base_directory, filename)


class TFRecordFeatureWriter(object):
    def __init__(self, queue, directory):
        self._directory = directory
        logger.info('directory: {directory}'.format(
            directory=self._directory
        ))
        if not os.path.exists(self._directory):
            os.makedirs(self._directory)
        self.queue = queue
        self._writer_list = []

    def _get_filepath(self, filename, suffix='pid0', ext='tfrecord'):
        # P: Pid; C: Count
        filename = '{filename}_P{suffix}_C.{ext}'.format(
            filename=filename,
            suffix=suffix,
            ext=ext
        )
        return os.path.join(self._directory, filename)

    def _tfrecord_writer_gen(self, filename, worker_num=1):
        """
        :param base_name: basedir name
        :param filename: file prefix name
        :param worker_num: workers number
        :return: writers based on workers
        """
        for i in range(worker_num):
            file_path = self._get_filepath(
                filename=filename,
                suffix=str(i)
            )
            yield tf.python_io.TFRecordWriter(file_path), file_path

    def _write_tfrecord(self, writer, generator_name, path, timeout=10):
        logger.info('PID: %d Writer starting...' % (os.getpid(),))
        count = 0
        while True:
            try:
                obj = self.queue.get(timeout=timeout)
            except:
                writer.close()
                break
            else:
                generator = getattr(obj, generator_name)()
                for example in generator:
                    writer.write(record=example.SerializeToString())
                    count += 1
        base, ext = os.path.splitext(path)
        new_path = base + str(count) + ext
        os.rename(path, new_path)
        logger.info('PID: %d Writer closed, count: %d \n    -> File saved: %s'
                    % (os.getpid(), count, new_path))

    def start(self, generator_name, filename, worker_num=None):
        worker_num = self._get_worker_num(worker_num)
        for _writer, filepath in self._tfrecord_writer_gen(filename, worker_num):
            writer = multiprocessing.Process(
                target=self._write_tfrecord,
                args=(_writer, generator_name, filepath)
            )
            writer.start()
            self._writer_list.append(writer)

    def join(self):
        """阻塞主进程"""
        for writer in self._writer_list:
            writer.join()

    def _get_worker_num(self, worker_num=None):
        """ For best practice:
        https://stackoverflow.com/questions/20039659/python-multiprocessings
        -pool-process-limit
        :param worker_num:
        :return:
        """
        worker_num = worker_num or multiprocessing.cpu_count()
        return worker_num


class TFRecordReader(object):
    '''
        1. self._feature_defs: feature的定义，比如:
            eg:
                self._feature_defs = {
                    'word':tf.FixedLenFeature([self.max_seq_length],tf.int64),
                    'pos':tf.FixedLenFeature([self.max_seq_length],tf.int64),
                    'length':tf.FixedLenFeature([1],tf.int64),
                    'entity':tf.FixedLenFeature([self.max_seq_length],tf.int64)
                }
        2. self.batch_size
            eg:
                self.batch_size = 256
        3. _decode: 对feature进行decode
            eg:
                def _decode(self,features):
                    word = tf.cast(features['word'],tf.int32)
                    pos = tf.cast(features['pos'],tf.int32)
                    length = tf.cast(features['length'],tf.int32)
                    entity = tf.cast(features['entity'],tf.int32)
                    return [word,pos,length,entity]

    '''

    def __init__(self, feature_defs, batch_size, tfrecord_dir, decode_func, num_epochs):
        self._feature_defs = feature_defs
        self._batch_size = batch_size
        self._tfrecord_dir = tfrecord_dir
        self._decode = decode_func

        self._threads = 3
        self._num_epochs = num_epochs

    def _read(self, filename_queue):
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(
            serialized_example,
            features=self._feature_defs
        )
        return features

    def read_and_decode(self, filename_queue):
        features = self._read(filename_queue)
        return self._decode(features)

    def get_tfrecord_filename(self):
        import glob
        tfrecord_file_list = glob.glob(os.path.join(self._tfrecord_dir, '*.tfrecord'))
        return tfrecord_file_list

    def input_pipeline(self):
        filename_list = self.get_tfrecord_filename()
        filename_queue = tf.train.string_input_producer(
            filename_list, num_epochs=self._num_epochs, shuffle=True
        )
        features_decoded_list = [
            self.read_and_decode(filename_queue) for _ in range(self._threads)
        ]

        min_after_dequeue = 10000
        capacity = min_after_dequeue + 3 * self._batch_size
        features_decoded_batch = tf.train.shuffle_batch_join(
            features_decoded_list, batch_size=self._batch_size, capacity=capacity,
            min_after_dequeue=min_after_dequeue
        )
        return features_decoded_batch


def view_tfrecord(directory):
    import glob
    tfrecord_file_list = glob.glob(os.path.join(directory, '*.tfrecord'))
    for tfrecord in tfrecord_file_list:
        for example in tf.python_io.tf_record_iterator(tfrecord):
            result = tf.train.Example.FromString(example)
            print(result)
