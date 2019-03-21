# coding: utf-8
import os
import jieba
from jieba.posseg import cut
import redis
rclient = redis.Redis(db=0)
cwd = os.path.dirname(os.path.abspath(__file__))
dict_dir = os.path.abspath(os.path.join(cwd, '..', 'nlp/corpus/'))


def load_dict(dict_list):
    if not isinstance(dict_list, list):
        dict_list = [dict_list]
    for user_dict in dict_list:
        dict_path = os.path.join(dict_dir, user_dict)
        if os.path.isfile(dict_path):
            jieba.load_userdict(dict_path)
            print('Load User Dict in %s' % dict_path)


def transform_text(text, strip=True, limit=None, join=False):
    load_dict(['user_dict.txt'])
    ignore_pos = ('c', 'd', 'e', 'g', 'j', 'o', 'p', 'u', 'uj', 'e', 'x', 'y', 'z', 'w')
    if strip:
        stopwords = rclient.get('STOPWORDS')
        if not stopwords:
            with open('../corpus/stopwords.txt', 'r') as f:
                stopwords_set = set()
                for line in f.readlines():
                    stopwords_set.add(line)
                rclient.set('STOPWORDS', stopwords_set)
        stopwords = stopwords.decode('utf-8')
    else:
        stopwords = ()

    words = filter(lambda x: x.word not in stopwords and x.flag not in ignore_pos, cut(text))
    if limit and limit > 0:
        words = list([w.word for w in words])[:limit]
    else:
        words = list([w.word for w in words])
    return words if not join else ' '.join(words)


def fin_cut(text, strip=True, limit=None, join=False):
    load_dict(['stock_words.txt'])
    return transform_text(text=text, strip=strip, limit=limit, join=join)
