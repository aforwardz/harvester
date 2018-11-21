# coding: utf-8
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from soccer import choices

# Create your models here.


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
        choices=choices.AWARD,
        default='0'
    )
    award_grade = models.CharField(
        verbose_name='获奖级别',
        choices=choices.AWARD_GRADE,
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


class League(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class Club(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class NationTeam(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class Person(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

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
        blank=True,
        default=''
    )
    nick_name = ArrayField(
        models.CharField,
        verbose_name='昵称',
        blank=True
    )
    gender = models.CharField(
        verbose_name='性别',
        choices=choices.GENDER,
        default='0'
    )
    height = models.FloatField(
        verbose_name='身高',
        blank=True,
        null=True
    )
    birth = models.DateField(
        verbose_name='出生日期',
        blank=True,
        null=True
    )
    age = models.PositiveIntegerField(
        verbose_name='年龄',
        blank=True,
        null=True
    )
    avatar = models.URLField(
        verbose_name='头像',
        blank=True,
        null=True
    )
    nationality = models.CharField(
        verbose_name='国籍',
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class Player(Person):
    club = models.ForeignKey(
        Club,
        verbose_name='俱乐部',
        related_name='players',
        on_delete=models.SET_NULL
    )
    foot = models.CharField(
        verbose_name='',
        max_length=10,
        choices=choices.FOOT,
        blank=True,
        default='-'
    )
    field = models.CharField(
        verbose_name='角色',
        choices=choices.FIELD,
        default='-'
    )
    positions = ArrayField(
        models.CharField,
        verbose_name='位置',
        blank=True
    )
    number = models.IntegerField(
        verbose_name='号码',
        blank=True,
        null=True
    )

    price = models.FloatField(
        verbose_name='身价(欧元)',
        blank=True,
        null=True
    )
    joined = models.DateField(
        verbose_name='加盟日期',
        blank=True,
        null=True,
    )
    contract_util = models.DateField(
        verbose_name='合同截止日期',
        blank=True,
        null=True
    )

    nation_team = models.ForeignKey(
        NationTeam,
        verbose_name='国家队',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class PlayRecord(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class Coach(Person):
    club = models.OneToOneField(
        Club,
        verbose_name='俱乐部',
        related_name='coach',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class TeachRecord(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class Game(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class GamePerformance(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class LeaguePerformance(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class NationPerformance(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class LeagueData(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )
