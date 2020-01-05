#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from django import forms
from chandeleur_app import models

logger = logging.getLogger('chandeleur_app.forms')


class ClubForm(forms.ModelForm):
    class Meta:
        model = models.Club
        fields = ('name',)


class RegistrationForm(forms.ModelForm):

    first_name = forms.ModelChoiceField(
        queryset=models.RegisteredPerson.objects.only("first_name"),
        widget=forms.TextInput(attrs={'id': "first_name", 'name': "first_name"},),
    )

    last_name = forms.ModelChoiceField(
        queryset=models.RegisteredPerson.objects.only("last_name"),
        widget=forms.TextInput(attrs={'id': "last_name", 'name': "last_name"},),
    )

    birth_date = forms.ModelChoiceField(required=False,
        queryset=models.RegisteredPerson.objects.only("birth_date"),
        widget=forms.TextInput(attrs={'id': "birth_date", 'name': "birth_date"},),
    )

    city = forms.ModelChoiceField(required=False,
        queryset=models.RegisteredPerson.objects.only("city"),
        widget=forms.TextInput(attrs={'id': "city", 'name': "city"},),
    )

    club_name = forms.ModelChoiceField(required=False,
        queryset=models.Club.objects.only("name"),
        widget=forms.TextInput(attrs={'id': "club_name", 'name': "club_name"},),
    )

    CHOICE_LIST = list()
    for license in models.License.objects.all():
        CHOICE_LIST.append((license.id, license.name))
    CHOICE_LIST.insert(0, ('', '-------'))
    license_name = forms.ChoiceField(required=False, choices=CHOICE_LIST)

    number_license = forms.ModelChoiceField(required=False,
        queryset=models.RegisteredPerson.objects.only("number"),
        widget=forms.TextInput(attrs={'id': "license_number", 'name': "license_number"},),
    )

    female = 'femme'
    male = 'homme'
    SEX_CHOICES = (
        (female, u"Femme"),
        (male, u"Homme")
    )
    sex = forms.ChoiceField(choices=SEX_CHOICES, widget=forms.RadioSelect(attrs={'id': "sex", 'name': "sex"}))

    free = 0
    pay = 3
    PRICE_CHOICES = (
        (free, u"Gratuit"),
        (pay, u"3 €")
    )
    price = forms.ChoiceField(choices=PRICE_CHOICES, widget=forms.RadioSelect(attrs={'id': "price", 'name': "price"}))

    trip_size = forms.ChoiceField(choices=[(t.id, t.name) for t in models.TripSize.objects.all()])

    class Meta:
        model = models.RegisteredPerson
        fields = (
            'first_name',
            'last_name',
            'birth_date',
            'city',
            'club_name',
            'license_name',
            'number_license',
            'sex',
            'price',
            'trip_size',
        )
