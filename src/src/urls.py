# Written by Andrew Perera
# Copyright 2019

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_auth.urls')),
    path('api/v1/', include('accounts.urls'))
]
