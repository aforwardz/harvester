# coding: utf-8
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField
from ner import models


class LabelSerializer(ModelSerializer):

    class Meta:
        model = models.Label
        fields = ('name', 'color')


class LabelProjectSerializer(ModelSerializer):
    labels = LabelSerializer(read_only=True, many=True)

    class Meta:
        model = models.LabelProject
        fields = ('project', 'labels')
