# coding: utf-8
import redis
import json
from collections import Counter
from django.conf import settings
from utils.queryset_iterator import queryset_iterator
from utils.utilities import Singleton


class DictionaryBuilder(metaclass=Singleton):
    def __init__(self, size=5000):
        self.dictionary_size = size
        self.rc = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        self._load_stopwords()

    def _load_stopwords(self):
        if self.rc.exists('stopwords'):
            self.stopwords = self.rc.get('stopwords')
        else:
            try:
                with open(settings.STOPWORDS, 'r') as f:
                    content = f.read()
                    self.stopwords = set(content.split('\n'))
                    self.rc.set('stopwords', self.stopwords)
            except:
                self.stopwords = set()
        assert self.stopwords, '无法导入停用词'

    def _is_stopword(self, word):
        return True if word in self.stopwords else False

    def build_dictionary_from_queryset(self, queryset):
        """
        :param queryset: 种子数据
        :return: 新词典
        """
        word_list = []
        for q in queryset_iterator(queryset):
            word_list.extend(list([
                w for w in w_l for w_l in w_2_l for w_2_l in q.words['word']
                if not self._is_stopword(w)]))
        counter = Counter(word_list)
        words, _ = list(zip(*counter.most_common(
            self.dictionary_size)))
        del counter
        dictionary, re_dictionary = dict(), dict()
        for i, w in enumerate(words):
            dictionary[w] = i + 1
            re_dictionary[i+1] = w
        with open(settings.DICTIONARY, 'w') as f:
            json.dump(dictionary, f)
        with open(settings.RE_DICTIONARY, 'w') as rf:
            json.dump(re_dictionary, rf)
        print('成功字典生成！')

