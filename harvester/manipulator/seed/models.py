# coding: utf-8
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from seed.choices import CONTENT_TYPES, USAGE_TYPES

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
        verbose_name='数据源',
        max_length=50,
        blank=True,
        default=''
    )
    usage = models.CharField(
        verbose_name='数据用途',
        choices=USAGE_TYPES,
        blank=True,
        default='0'
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
        default='0'
    )

    words = JSONField(
        verbose_name='文本分词',
        blank=True,
        default={}
    )

    objects = SeedManager

    def __str__(self):
        return str(self.id) + '--' + self.get_content_type_display()

    class Meta:
        verbose_name = verbose_name_plural = '种子数据'
