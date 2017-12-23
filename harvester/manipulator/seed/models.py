from django.db import models

# Create your models here.


class SeedManager(models.Manager):
    pass


class Seed(models.Model):
    create_time = models.DateTimeField(
        verbose_name='',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        verbose_name='',
        auto_now=True
    )

    content = models.TextField(
        verbose_name='',
        blank=True
    )
    clean_content = models.TextField(
        verbose_name='',
        blank=True
    )
