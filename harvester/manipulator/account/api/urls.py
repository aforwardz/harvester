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
            ),
    re_path(r'^wxlogin/$',
            views.WXLoginView.as_view(),
            name="wxlogin_view",
            ),
    re_path(r'^wxdata/$',
            views.WXAccountDataUpdateView.as_view(),
            name="wxdata_update_view",
            ),
    re_path(r'^ulogin/$',
            views.UnionLoginView.as_view(),
            name="union_login_view",
            ),
    re_path(r'^uauth/$',
            views.UnionAccountAuthorizeView.as_view(),
            name="union_account_authorize_view",
            ),
    re_path(r'^udata/$',
            views.UnionAccountDataUpdateView.as_view(),
            name="union_account_data_update_view",
            )
]
