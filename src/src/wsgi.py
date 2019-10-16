# Written by Andrew Perera
# Copyright 2019


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'custom_user.settings')

application = get_wsgi_application()
