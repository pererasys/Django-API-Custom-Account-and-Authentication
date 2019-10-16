# Written by Andrew Perera
# Copyright 2019

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('accounts')

    def ready(self):
        import accounts.signals
