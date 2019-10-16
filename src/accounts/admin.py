# Written by Andrew Perera
# Copyright 2019

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import *  # pylint: disable=unused-wildcard-import

Account = get_user_model()

# User Accounts
admin.site.register(Account)

# Verification Codes
admin.site.register(VerificationCode)

# Unregister groups (not using)
admin.site.unregister(Group)
