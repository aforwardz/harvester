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


class Competition(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    name = models.CharField(
        verbose_name='赛事名称',
        max_length=50,
        blank=True
    )

    short_name = models.CharField(
        verbose_name='赛事简称',
        max_length=30,
        blank=True,
        default=''
    )

    en_name = models.CharField(
        verbose_name='赛事英文名称',
        max_length=100,
        blank=True,
        default=''
    )

    nation = models.CharField(
        verbose_name='赛事国别',
        max_length=30,
        blank=True
    )

    season = models.CharField(
        verbose_name='赛季',
        max_length=30,
        blank=True,
        null=True
    )


class Team(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    name = models.CharField(
        verbose_name='名称',
        max_length=50,
        blank=True
    )

    short_name = models.CharField(
        verbose_name='简称',
        max_length=30,
        blank=True,
        default=''
    )

    en_name = models.CharField(
        verbose_name='英文名称',
        max_length=100,
        blank=True,
        default=''
    )

    attr = models.CharField(
        verbose_name='性质',
        max_length=30,
        choices=choices.TEAM_ATTR,
        blank=True
    )

    level = models.CharField(
        verbose_name='级别',
        max_length=30,
        blank=True,
        null=True
    )

    nation = models.CharField(
        verbose_name='赛事国别',
        max_length=30,
        blank=True
    )

    competitions = models.ManyToManyField(
        Competition,
        verbose_name='赛事',
        related_name='teams',
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
        Team,
        verbose_name='俱乐部',
        related_name='players',
        null=True,
        on_delete=models.SET_NULL
    )
    nation_team = models.ForeignKey(
        Team,
        verbose_name='国家队',
        related_name='players',
        null=True,
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


class Match(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class PlayerMatchPerformance(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class PlayerCompetitionPerformance(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class PlayerNationPerformance(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )


class CompetitionData(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )
