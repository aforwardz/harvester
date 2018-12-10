# coding:utf-8
from django.urls import re_path
from account.api import views

urlpatterns = [
    re_path(r'^login/$',
            views.AccountLoginView.as_view(),
            name="account_login_view",
            ),
    re_path(r'^logout/$',
            views.AccountLogoutView.as_view(),
            name="account_logout_view",
            )
]
