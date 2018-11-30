# coding:utf-8
from django.urls import re_path
from nlp import views

urlpatterns = [
    re_path(r'^cut/$',
            views.ContentCutView.as_view(),
            name='content_cut_view'),
    re_path(r'^ner/$',
            views.ContentNerView.as_view(),
            name='content_ner_view'),
]
