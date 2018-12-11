# coding: utf-8
# 句子关系抽取器
import os
import re
import jieba
from jieba.posseg import cut
from processor import choices
from processor.preprocess import transform_text

cwd = os.path.dirname(os.path.abspath(__file__))
user_dict = os.path.abspath(os.path.join(cwd, '..', 'nlp/corpus/user_dict.txt'))
print(user_dict)
if os.path.isfile(user_dict):
    jieba.load_userdict(user_dict)


class SoccerTripleExtractor(object):
    def __init__(self):
        pass

    def _get_word_list(self, sentence):
        self.word_list = transform_text(sentence)

    def is_multiple(self):
        for word in self.word_list:
            if word in choices.MULTIPLE_WORDS:
                return True
        return False

    def _get_subject(self):
        for word in self.word_list:
            pass

    def construct_cypher(self):
        pass