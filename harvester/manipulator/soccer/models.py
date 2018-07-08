# coding: utf-8
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from soccer.choices import (
    GENDER,
    AWARD,
    AWARD_GRADE,
    FIELD
)

# Create your models here.


class Club(models.Model):
    pass


class Award(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    award_name = models.CharField(
        verbose_name='奖项名称',
        choices=AWARD,
        default='0'
    )
    award_grade = models.CharField(
        verbose_name='获奖级别',
        choices=AWARD_GRADE,
        default='0'
    )
    award_season = models.CharField(
        verbose_name='获奖赛季',
        max_length=20,
        blank=True
    )
    award_date = models.DateField(
        verbose_name='获奖日期',
        blank=True
    )


class Person(models.Model):
    name = models.CharField(
        verbose_name='名字',
        max_length=50
    )
    alias = ArrayField(
        models.CharField,
        verbose_name='别名',
        blank=True
    )
    en_name = models.CharField(
        verbose_name='英文名',
        max_length=100,
        blank=True
    )
    nick_name = ArrayField(
        models.CharField,
        verbose_name='昵称',
        blank=True
    )
    gender = models.CharField(
        verbose_name='性别',
        choices=GENDER,
        default='0'
    )
    birth = models.DateField(
        verbose_name='出生日期',
        blank=True
    )
    age = models.PositiveIntegerField(
        verbose_name='年龄',
        blank=True
    )
    nation = models.CharField(
        verbose_name='国籍',
        max_length=20,
        blank=True
    )

    class Meta:
        abstract = True


class Player(Person):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    current_club = models.ForeignKey(
        Club,
        verbose_name='当前所在俱乐部',
        on_delete=models.SET_NULL
    )
    field = models.CharField(
        verbose_name='角色',
        choices=FIELD,
        default='0'
    )
    positions = ArrayField(
        models.CharField,
        verbose_name='位置',
        blank=True
    )

