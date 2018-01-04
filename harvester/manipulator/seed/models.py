# coding: utf-8
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from seed.choices import CONTENT_TYPES

# Create your models here.


class SeedManager(models.Manager):
    pass


class Seed(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )
    source = models.CharField(
        verbose_name='',
        max_length=50,
        blank=True,
        default=''
    )

    content = models.TextField(
        verbose_name='文本',
        blank=True
    )
    clean_content = models.TextField(
        verbose_name='清洗文本',
        blank=True
    )

    content_type = models.CharField(
        verbose_name='文本归类(大类)',
        choices=CONTENT_TYPES,
        blank=True,
        default=0
    )

    words = JSONField(
        verbose_name='文本分词',
        blank=True,
        default={}
    )

    objects = SeedManager


    # word
