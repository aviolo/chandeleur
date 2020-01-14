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
        label="Prénom",
        queryset=models.RegisteredPerson.objects.all(),
        widget=forms.TextInput(),
    )

    last_name = forms.ModelChoiceField(
        label="Nom",
        queryset=models.RegisteredPerson.objects.all(),
        widget=forms.TextInput(),
    )

    birth_date = forms.ModelChoiceField(
        label="Date de naissance",
        required=False, queryset=models.RegisteredPerson.objects.all(),
        widget=forms.TextInput(),
    )

    city = forms.ModelChoiceField(
        label="Ville",
        required=False, queryset=models.RegisteredPerson.objects.all(),
        widget=forms.TextInput(),
    )

    club_name = forms.ModelChoiceField(
        label="Nom du club",
        required=False, queryset=models.Club.objects.all(),
        widget=forms.TextInput(),
    )

    license = forms.ModelChoiceField(
        label="Nom de license",
        required=False,
        queryset=models.License.objects.all(),
        empty_label='------',
    )

    license_number = forms.ModelChoiceField(
        label="Numéro de license",
        required=False, queryset=models.License.objects.all(),
        widget=forms.TextInput(),
    )

    female = 'femme'
    male = 'homme'
    SEX_CHOICES = (
        (female, u"Femme"),
        (male, u"Homme")
    )
    sex = forms.ChoiceField(label="Sexe", choices=SEX_CHOICES, widget=forms.RadioSelect())

    free = 0
    pay = 3
    PRICE_CHOICES = (
        (free, u"Gratuit"),
        (pay, u"3 €")
    )

    price = forms.ChoiceField(label="Tarif", choices=PRICE_CHOICES, widget=forms.RadioSelect())

    trip_size = forms.ModelChoiceField(
        label="Taille du parcour",
        required=True,
        queryset=models.TripSize.objects.all(),
    )

    class Meta:
        model = models.RegisteredPerson
        fields = (
            'first_name',
            'last_name',
            'birth_date',
            'city',
            'club_name',
            'license',
            'license_number',
            'sex',
            'price',
            'trip_size',
        )
