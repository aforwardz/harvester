from django.contrib.auth.models import User
from django.db import models
from account.choices import IDENTITY

# Create your models here.


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
