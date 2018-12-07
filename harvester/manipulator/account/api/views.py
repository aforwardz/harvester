# coding: utf-8
import requests
import json
import redis
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from account.api import serializers
from account.models import Account


class AccountLoginView(APIView):
    serializer_class = serializers.AccountSerializer

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                try:
                    account = Account.objects.get(user=user)
                except:
                    raise AuthenticationFailed('未创建对应账户，联系管理员')
                return Response({'detail': '登录成功'}, status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed('用户名或密码错误')
        except ObjectDoesNotExist:
            raise AuthenticationFailed('没有该用户，联系管理员')


class AccountLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response('退出成功')
