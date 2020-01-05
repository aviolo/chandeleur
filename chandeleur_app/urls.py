#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from chandeleur_app import views

urlpatterns = [
    # login, logout and password reset
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^ajax/search/(?P<input_name>[-_\w\d]{1,200})$', views.user_search, dict(ajax=True), name='ajax-search'),
    url(r'^add_user$', views.add_user, name='chandeleur_app-home_view'),
    url(r'^statistiques$', views.statistiques, name='chandeleur_app-statistiques'),
    url(r'^$', views.home_view, name='chandeleur_app-home_view'),
]
