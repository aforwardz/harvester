import json
import jieba
from jieba.posseg import cut
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from account.models import Account
from ner.models import LabelProject, Label
from ner import serializers
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


class LabelProjectRetrieveCreateView(APIView):
    permission_classes = ()
    http_method_names = ('post',)

    def post(self, request):
        ac = Account.objects.get(user=request.user)
        if not request.data.get('project'):
            return Response({'detail': '', 'status': 'ERROR'})
        action = request.data.get('action')
        if action == 'add':
            if ac.identity == 'normal' and ac.label_pros.exists():
                return Response({'detail': '', 'status': 'ERROR'})
            label_pro, _ = LabelProject.objects.get_or_create(project=request.data.get('project'), creator=ac)
            label_pro.labels.clear()
            print(request.data.get('labels'))
            for l in request.data.get('labels'):
                label, _ = Label.objects.get_or_create(**l)
                label_pro.labels.add(label)
            label_pro.save()
            return Response({'detail': '', 'status': 'OK'})
        elif action == 'delete':
            ac.label_pros.filter(project=request.data.get('project')).delete()
            return Response({'detail': '', 'status': 'OK'})
        else:
            return Response({'detail': '', 'status': 'ERROR'})

    def get(self, request):
        try:
            ac = Account.objects.get(user=request.user)
            return Response({'data': serializers.LabelProjectSerializer(ac.label_pros.all(), many=True),
                             'status': 'OK'})
        except ObjectDoesNotExist:
            return Response({'data': [], 'status': 'ERROR'})


class ContentLabelView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ('post',)

    def post(self, request):
        content = request.data.get('content')
        sentences = content.split('\n')
        result_2_list = []
        for sentence in sentences:
            result_2_list.append(list([{'word': word.word,
                                        'pos_n': JIEBA_POS_DICT.get(word.flag, '未知'),
                                        'ner': 'unknown',
                                        'ner_n': '未知'}
                                       for word in cut(sentence)]))
        return Response({'data': result_2_list, 'status': 200})
