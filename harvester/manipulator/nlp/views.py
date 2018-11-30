import json
import jieba
from jieba.posseg import cut
from rest_framework.views import APIView
from rest_framework.response import Response
from nlp.choices import JIEBA_POS_DICT


class ContentCutView(APIView):
    http_method_names = ('post',)

    def post(self, request):
        content = request.data.get('content')
        sentences = content.split('\n')
        result_2_list = []
        for sentence in sentences:
            result_2_list.append(list([{'word': word.word,
                                        'pos': word.flag,
                                        'pos_n': JIEBA_POS_DICT.get(word.flag, '未知')}
                                       for word in cut(sentence)]))
        return Response({'data': result_2_list, 'status': 200})


class ContentNerView(APIView):
    http_method_names = ('post',)

    def post(self, request):
        content = request.data.get('content')
        sentences = content.split('\n')
        result_2_list = []
        return Response({'data': result_2_list, 'status': 200})
