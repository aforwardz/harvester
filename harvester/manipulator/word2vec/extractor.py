# coding: utf-8
import tensorflow as tf
from django.conf import settings
from seed.models import Seed
from processor.searcher import Searcher


class WordFeatureExtractor(object):
    def __init__(self):
        self.context_size = settings.CONTEXT_SIZE
        self.searcher = Searcher()

    def _get_word_pos_2_list(self, obj):
        pos_item_2_list = getattr(obj, 'pos')
        word_2_list, pos_2_list = [], []
        for pos_item_list in pos_item_2_list:
            word_list, pos_list = [], []
            for item in pos_item_list:
                word_list.append(item.get('word'))
                pos_list.append(item.get('pos'))
            word_2_list.append(word_list)
            pos_2_list.append(pos_list)

        return word_2_list, pos_2_list

    def _get_word_context(self, index, word_list, pos_list):
        pass

    def word_feature_generator(self, obj):
        word_2_list, pos_2_list = self._get_word_pos_2_list(obj)

        for word_list, pos_list in zip(word_2_list, pos_2_list):
            word_index_list = self.searcher.search_word_index(word_list)

            context_2_list = [self._get_word_context(
                index, word_list, pos_list) for _, index in enumerate(word_list)]
            context_index_2_list = [self.searcher.search_word_index(
                context_list) for context_list in context_2_list]

            for index, _ in enumerate(word_list):
                feature = {}
                feature['word'] = tf.train.Feature(
                    int64_list=tf.train.Int64List(
                        value=[word_index_list[index]]
                    )
                )
                feature['context'] = tf.train.Feature(
                    int64_list=tf.train.Int64List(
                        value=context_index_2_list[index]
                    )
                )

                example = tf.train.Example(
                    features=tf.train.Features(feature=feature)
                )
                yield example

