#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('chandeleur_app.urls')),
]
