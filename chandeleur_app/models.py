#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # checker que le profil associé à l'utilisateur existe
    # user.get_profile()
    # This field is required.
    user = models.OneToOneField(User, on_delete=models.CASCADE)


def create_user_profile(sender, instance, created, **kwargs):
    if sender == User and created is True:
        profile = UserProfile(user=instance)
        profile.save()
    return None


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


class registered_person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField('birth date', default=datetime.datetime.now)
    city = models.CharField(max_length=255)
    number_license = models.CharField(max_length=255)
    club_name = models.ForeignKey(Club, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    trip_size = models.ForeignKey(TripSize, on_delete=models.CASCADE)
    sex = models.BooleanField(default=True)
    present = models.BooleanField(default=False)


models.signals.post_save.connect(receiver=create_user_profile, sender=User, weak=False, dispatch_uid='create_user_profile')
