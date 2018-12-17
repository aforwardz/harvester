import re
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from account.choices import IDENTITY

# Create your models here.


def validate_color(color):
    if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
        raise ValidationError('%s是非法HEX颜色字符串' % color)


class Label(models.Model):
    name = models.CharField(
        verbose_name='标签名',
        max_length=50
    )

    color = models.CharField(
        verbose_name='颜色',
        max_length=10,
        validators=[validate_color]
    )


class LabelProject(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    project = models.CharField(
        verbose_name='项目名',
        max_length=50
    )

    labels = models.ManyToManyField(
        Label,
        related_name='projects'
    )

    creator = models.ForeignKey(
        'Account',
        related_name='label_pros',
        on_delete=models.CASCADE
    )


class Account(models.Model):
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name='用户',
        related_name='account',
        on_delete=models.CASCADE
    )

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    nickname = models.CharField(
        verbose_name='昵称',
        max_length=50,
        blank=True,
        default=''
    )
    real_name = models.CharField(
        verbose_name='真实姓名',
        max_length=50,
        blank=True,
        default=''
    )

    identity = models.CharField(
        verbose_name='身份',
        max_length=20,
        choices=IDENTITY,
        blank=True,
        default='normal'
    )

    def __str__(self):
        return self.real_name or self.nickname

    class Meta:
        verbose_name = verbose_name_plural = 'NLPer'
