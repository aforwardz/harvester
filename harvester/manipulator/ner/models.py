import re
from django.db import models
from django.core.exceptions import ValidationError
from account.models import Account

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

    def __str__(self):
        return self.name + ' : ' + self.color

    class Meta:
        verbose_name = verbose_name_plural = '标注设置'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.capitalize()
        super(Label, self).save(force_insert=force_insert, force_update=force_update,
                                using=using, update_fields=update_fields)


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
        Account,
        related_name='label_pros',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.creator.nickname + ' : ' + self.project

    class Meta:
        verbose_name = verbose_name_plural = '标注项目'
