#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.contrib.auth.models import User


class License(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'license %s' % self.name


class Club(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'association %s' % self.name


class TripSize(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'association %s' % self.name


class RegisteredPerson(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField('birth date', default=datetime.datetime.now, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    club_name = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)
    license = models.ForeignKey(License, on_delete=models.CASCADE, blank=True, null=True)
    number_license = models.CharField(max_length=255, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    trip_size = models.ForeignKey(TripSize, on_delete=models.CASCADE)
    sex = models.BooleanField(default=True)
    present = models.BooleanField(default=False)
    user_in_charge = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
