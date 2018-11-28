import jieba
from jieba.posseg import cut
import redis

# jieba.load_userdict('../dictionary/userdict.txt')
rclient = redis.Redis(db=0)


def transform_text(text, strip=True, limit=None, join=False):
    if strip:
        stopwords = rclient.hget('STOPWORDS')
        if not stopwords:
            with open('../corpus/stopwords.txt', 'r') as f:
                stopwords_set = set()
                for line in f.readlines():
                    stopwords_set.add(line)
                rclient.set('STOPWORDS', stopwords_set)
        stopwords = stopwords.decode('utf-8')
    else:
        stopwords = ()

    words = filter(lambda x: x.word not in stopwords and x.flag != 'x', cut(text))
    if limit and limit > 0:
        words = list([w.word for w in words])[:limit]
    else:
        words = list([w.word for w in words])
    return words if not join else ' '.join(words)
