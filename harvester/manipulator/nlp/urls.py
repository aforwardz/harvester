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
    re_path(r'^label/$',
            views.ContentLabelView.as_view(),
            name='content_label_view'),
    re_path(r'^label_pro/$',
            views.LabelProjectRetrieveCreateView.as_view(),
            name='label_project_retrieve_create_view')
]
