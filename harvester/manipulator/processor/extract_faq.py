# coding: utf-8
import re
import csv
from django.core.management.base import BaseCommand
from news.models import News
from datetime import datetime, timedelta
from utils.queryset_iterator import queryset_iterator
from nlp.preprocess import transform_text
from sklearn.externals import joblib


class Command(BaseCommand):
    in_rules = ('怎', '啥', '哪', '如何', '为何', '有何', '什么',
                '还是', '是否', '是不是', '多少', '多久',
                '多快', '多长', '多远', '吗', '嘛', )

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        count = 0
        queryset = News.objects.using('test').filter(news_type='2', create_time__lt='2018-06-01')
        print('Queryset Count : ', queryset.count())
        pipeline = joblib.load('./nlp/classify_model.pkl')
        skip = False
        faq_pairs = []
        batch = 0

        for q in queryset_iterator(queryset=queryset):
            print(q.news_id)
            paragraph_list = re.split(r'[\t\n\r]', q.content)
            for index, paragraph in enumerate(paragraph_list):
                if len(faq_pairs) >= 1000:
                    with open('question_list_' + str(batch) + str(batch) + '.csv', 'w', newline='') as f:
                        writer = csv.writer(f, dialect='excel', delimiter=',')
                        writer.writerows(faq_pairs)
                    faq_pairs = []
                    batch += 1
                if skip:
                    skip = False
                    continue
                p_t = pipeline.predict([transform_text(paragraph)]).tolist()[0]
                if p_t != '2':
                    continue
                sentence_list = re.split(r'[？]', paragraph)
                s_t = pipeline.predict([transform_text(sentence_list[0])]).tolist()[0]
                if s_t != '2':
                    continue
                if len(sentence_list) == 1 and any([paragraph.endswith(t) for t in ('?', '？', '吗', '什么')]):
                    if 10 < len(sentence_list[0]) < 60 and any([tag in sentence_list[0] for tag in self.in_rules]) \
                            and index + 1 < len(paragraph_list) and len(paragraph_list[index + 1].strip()) > 50:
                        count += 1
                        print('q: ', sentence_list[0])
                        print('a: ', paragraph_list[index + 1], '\n')
                        faq_pairs.append([sentence_list[0], paragraph_list[index + 1], q.link])
                        skip = True
                elif len(sentence_list) > 1:
                    if 10 < len(sentence_list[0]) < 60 and any([tag in sentence_list[0] for tag in self.in_rules]) \
                            and len(''.join(sentence_list[1:])) > 50:
                        count += 1
                        print('q: ', sentence_list[0])
                        print('a: ', ''.join(sentence_list[1:]), '\n')
                        faq_pairs.append([sentence_list[0], ''.join(sentence_list[1:]), q.link])

        if len(faq_pairs):
            with open('question_list_' + str(batch) + '.csv', 'w', newline='') as f:
                writer = csv.writer(f, dialect='excel', delimiter=',')
                writer.writerows(faq_pairs)
            faq_pairs = []
            batch += 1

        print('all question count: ', count)
