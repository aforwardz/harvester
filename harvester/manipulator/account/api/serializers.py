# coding: utf-8
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from account import models


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = ('id', 'nickname', 'real_name', )

