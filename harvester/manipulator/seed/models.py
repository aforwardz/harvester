# coding: utf-8
from django.db import models

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

    content = models.TextField(
        verbose_name='文本',
        blank=True
    )
    clean_content = models.TextField(
        verbose_name='清洗文本',
        blank=True
    )

    # word
