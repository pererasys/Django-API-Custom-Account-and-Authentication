# Written by Andrew Perera
# Copyright 2019

from django.urls import path, re_path, include
from .views import *

app_name = 'ACCOUNTS'


urlpatterns = [
    re_path('check-username/(?P<username>[\w]+)/$',
            CheckUsernameView.as_view(), name="check-username"),
    re_path('check-phonenumber/(?P<phonenumber>[0-9\+]+)/$',
            CheckPhoneNumberView.as_view(), name="check-phonenumber"),
    path('accounts/phone-verification/', PhoneVerificationView.as_view()),
    path('accounts/register/', RegisterView.as_view()),
]
