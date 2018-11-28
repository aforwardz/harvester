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
        max_length=10,
        choices=choices.AWARD,
        default='0'
    )
    award_grade = models.CharField(
        verbose_name='获奖级别',
        max_length=10,
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

    def __str__(self):
        return self.award_name

    class Meta:
        verbose_name = verbose_name_plural = '奖项'


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '赛事'


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

    class Meta:
        abstract = True


class Club(Team):
    competitions = models.ManyToManyField(
        Competition,
        verbose_name='赛事',
        related_name='clubs',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '俱乐部'


class NationTeam(Team):
    competitions = models.ManyToManyField(
        Competition,
        verbose_name='赛事',
        related_name='nations',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '国家队'


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
        models.CharField(max_length=50),
        verbose_name='别名',
        blank=True,
        default=[]
    )
    en_name = models.CharField(
        verbose_name='英文名',
        max_length=100,
        blank=True,
        default=''
    )
    nick_name = ArrayField(
        models.CharField(max_length=50),
        verbose_name='昵称',
        blank=True,
        default=[]
    )
    gender = models.CharField(
        verbose_name='性别',
        max_length=5,
        choices=choices.GENDER,
        default='0'
    )
    height = models.PositiveIntegerField(
        verbose_name='身高(CM)',
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
        null=True,
        on_delete=models.SET_NULL
    )
    nation_team = models.ForeignKey(
        NationTeam,
        verbose_name='国家队',
        related_name='players',
        null=True,
        on_delete=models.SET_NULL
    )
    foot = models.CharField(
        verbose_name='惯用脚',
        max_length=10,
        choices=choices.FOOT,
        blank=True,
        default='-'
    )
    field = models.CharField(
        verbose_name='角色',
        max_length=10,
        choices=choices.FIELD,
        default='-'
    )
    positions = ArrayField(
        models.CharField(max_length=10, choices=choices.POSITION),
        verbose_name='位置',
        blank=True,
        default=[]
    )
    number = models.IntegerField(
        verbose_name='号码',
        blank=True,
        null=True
    )

    price = models.PositiveIntegerField(
        verbose_name='身价(万欧元)',
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

    class Meta:
        verbose_name = verbose_name_plural = '球员'


class PlayRecord(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    def __str__(self):
        return ''

    class Meta:
        verbose_name = verbose_name_plural = '效力记录'


class Coach(Person):
    coach_club = models.OneToOneField(
        Club,
        verbose_name='俱乐部',
        related_name='coach',
        null=True,
        on_delete=models.SET_NULL
    )

    coach_nation = models.OneToOneField(
        NationTeam,
        verbose_name='俱乐部',
        related_name='coach',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '教练'


class CoachRecord(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    def __str__(self):
        return ''

    class Meta:
        verbose_name = verbose_name_plural = '执教记录'


class Match(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    def __str__(self):
        return ''

    class Meta:
        verbose_name = verbose_name_plural = '比赛'


class PlayerPerformance(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    def __str__(self):
        return ''

    class Meta:
        verbose_name = verbose_name_plural = '球员表现'


class CompetitionData(models.Model):
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='更新时间',
        auto_now=True
    )

    def __str__(self):
        return ''

    class Meta:
        verbose_name = verbose_name_plural = '赛事数据'
