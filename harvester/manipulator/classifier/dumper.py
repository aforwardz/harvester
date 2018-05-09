# coding: utf-8
# handle sogou news data
import re
import json
import random
import jieba
from jieba.posseg import cut
from django.core.cache import cache
from classifier.choices import SOHU_NEWS_TYPE


def handle_news(news_path):
    news = []
    p = re.compile('</doc>', re.S)
    t = re.compile(r'(?<=\<contenttitle\>).*(?=\<\/contenttitle\>)')
    c = re.compile(r'(?<=\<content\>).*(?=\<\/content\>)')
    u = re.compile(r'(?<=\<url\>).*(?=\<\/url\>)')
    l = re.compile(r'(?<=http://).*(?=\.com)')
    with open(news_path, 'r', encoding='gb18030') as f:
        parse_list = p.split(f.read())
        for pasrse in parse_list:
            if not u.findall(pasrse):
                continue
            label = l.findall(u.findall(pasrse)[0])
            if not label:
                continue
            label_index = ''
            label = label[0]
            for type in SOHU_NEWS_TYPE:
                if any([l in label for l in type[1]]):
                    label_index = type[0]
                    break
            if label_index and c.findall(pasrse):
                print(label_index, 'train')
                news.append({
                    'label': label_index,
                    'title': t.findall(pasrse)[0],
                    'content': c.findall(pasrse)[0]
                })

    with open('raw_news.txt', 'w', encoding='utf8') as n:
        json.dump(news, n)


def clean_news():
    stopwords = cache.get('STOPWORDS')
    print('stopwords', stopwords)
    if not stopwords:
        with open('../dictionary/stopwords.txt', 'r') as f:
            stopwords_list = set()
            for line in f.readlines():
                stopwords_list.add(line.strip('\n'))
            cache.set('STOPWORDS', stopwords_list)

    news_lines, news_labels = [], []
    with open('raw_news.txt', 'r',) as t:
        news = json.load(t)
        for raw in news:
            print(raw['label'])
            print(raw['title'])
            words = cut(raw['title'] + ' ' + raw['content'])
            words = filter(lambda x: x.word not in stopwords and x.flag != 'x', words)
            words = list([w.word for w in words])[:100]
            print(words)
            news_lines.append(' '.join(words) + '\n')
            news_labels.append(raw['label'] + '\n')

    assert len(news_labels) == len(news_lines), 'train data length not matched'
    with open('news.txt', 'w') as f_news:
        print(len(news_lines))
        f_news.writelines(news_lines)

    with open('news_label.txt', 'w') as f_news_label:
        print(len(news_labels))
        f_news_label.writelines(news_labels)

