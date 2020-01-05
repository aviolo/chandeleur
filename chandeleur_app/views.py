from datetime import datetime
import logging
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render

from chandeleur_app import forms
from chandeleur_app import models

# Create your views here.


logger = logging.getLogger('chandeleur_app.views')


# handle errors
def on_error(text, will_send_mail=True):
    logger.error(text)
    mails = [admin[1] for admin in settings.ADMINS]
    if will_send_mail:
        send_mail('Error from foyerduporteau.net', text, 'foyerduporteau@gmail.com', mails, fail_silently=False)


def home_view(request):
    user = None
    registration_form = None
    try:
        user = request.user
        if user.is_active:
            registration_form = forms.RegistrationForm(request.POST, instance=models.RegisteredPerson())
            nb_sign = models.RegisteredPerson.objects.all().filter(present=True).count()
            nb_register = models.RegisteredPerson.objects.all().filter(user_in_charge_id=user).count()
    except IndexError:
        pass
    return render(request, "chandeleur_app/home_view.html", {
        'registration_form': registration_form, 'nb_sign': nb_sign, 'nb_registered': nb_register,
    })


@login_required
def add_user(request):
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        user_registered = models.RegisteredPerson.objects.filter(first_name=first_name, last_name=last_name)
        if user_registered:
            if request.POST["birth_date"]:
                date_time_obj = datetime.strptime(request.POST["birth_date"], '%d/%m/%Y')
                user_registered[0].birth_date = date_time_obj
            else:
                user_registered[0].birth_date = None
            user_registered[0].city = request.POST["city"]
            if (len(request.POST.get("club_name"))):
                club_id = get_club_id_by_name(request.POST["club_name"])
                if not club_id:
                    club_id = add_new_club(request, request.POST["club_name"])
            else:
                club_id = None
            user_registered[0].club_name_id = club_id
            if (len(request.POST.get("license_name"))):
                license_id = get_license_id_by_name(request.POST["license_name"])
                user_registered[0].license_id = license_id
            if (len(request.POST.get("number_license"))):
                user_registered[0].number_license = request.POST["number_license"]
            user_registered[0].sex = False if request.POST["sex"] == "homme" else True
            user_registered[0].price = 0 if request.POST["price"] == "0" else 3
            user_registered[0].trip_size_id = request.POST["trip_size"]
            user_registered[0].present = True
            user_id = get_user_id_by_username(request.user)
            user_registered[0].user_in_charge_id = user_id
            user_registered[0].save()
        else:
            if (len(request.POST.get("club_name"))):
                club_id = get_club_id_by_name(request.POST["club_name"])
                if not club_id:
                    club_id = add_new_club(request, request.POST["club_name"])
            else:
                club_id = None
            if (len(request.POST.get("license_name"))):
                license = get_license_instance_by_id(request.POST.get("license_name"))
            else:
                license = None
            trip_size = get_trip_size_instance_by_id(request.POST.get("trip_size"))
            registered_person = models.RegisteredPerson()
            registered_person.first_name = request.POST["first_name"]
            registered_person.last_name = request.POST["last_name"]
            if request.POST["birth_date"]:
                date_time_obj = datetime.strptime(request.POST["birth_date"], '%d/%m/%Y')
                registered_person.birth_date = date_time_obj
            else:
                registered_person.birth_date = None
            registered_person.city = request.POST["city"]
            registered_person.club_name_id = club_id
            registered_person.license = license
            registered_person.number_license = request.POST["number_license"]
            sex = False if request.POST["sex"] == "homme" else True
            registered_person.sex = sex
            registered_person.price = request.POST["price"]
            registered_person.trip_size = trip_size
            registered_person.present = True
            user = get_user_instance_by_username(request.user)
            registered_person.user_in_charge = user
            registered_person.save()
        return HttpResponseRedirect('/')


@login_required
def user_search(request, input_name, ajax=False):
    term = request.GET.get('term', '').lower()
    models_filter = re.findall(r'model:([a-z0-9]+)', term)
    for m in models_filter:
        term = term.replace('model:%s' % m, '')
    term = term.strip()
    if input_name == "firstname" or input_name == "lastname":
        all_users_register = list()
        for all_users in models.RegisteredPerson.objects.all():
            add_user = False
            if input_name == "firstname":
                result = re.search(r'^%s[\w]*' % (term), all_users.first_name.lower())
                if result is not None:
                    add_user = True
                    label = all_users.first_name
            if input_name == "lastname":
                result = re.search(r'^%s[\w]*' % (term), all_users.last_name.lower())
                if result is not None:
                    add_user = True
                    label = all_users.last_name
            if add_user:
                club_name = get_club_name_by_id(all_users.club_name_id)
                license_name = get_license_name_by_id(all_users.license_id)
                # label = "%s %s" % (all_users.first_name, all_users.last_name)
                all_users_register.append({'label': label, 'first_name': all_users.first_name, 'last_name': all_users.last_name, 'birth_date': all_users.birth_date, 'city': all_users.city, 'club_name': club_name, 'license_name': license_name, 'license_number': all_users.number_license, 'sex': all_users.sex, 'price': all_users.price, 'trip_size': all_users.trip_size.name})
        if ajax:
            return JsonResponse(all_users_register, safe=False)
    if input_name == "clubname":
        club_name_register = list()
        for club_name in models.Club.objects.all():
            add_club = False
            result = re.search(r'^%s[\w]*' % (term), club_name.name.lower())
            if result is not None:
                add_club = True
            if add_club:
                print(club_name.name)
                club_name_register.append({'label': club_name.name, 'club_name': club_name.name})
        if ajax:
            return JsonResponse(club_name_register, safe=False)


def add_new_club(request, club_name):
    try:
        new_club = models.Club()
        new_club.name = club_name
        new_club.save()
        return new_club.id
    except IndexError as e:
        on_error('Error in add club name : %s' % e)


def get_user_instance_by_username(user_id):
    return models.User.objects.all().filter(username=user_id)[0]


def get_user_id_by_username(username):
    return models.User.objects.all().filter(username=username)[0].id


def get_trip_size_instance_by_id(trip_size_id):
    return models.TripSize.objects.all().filter(id=trip_size_id)[0]


def get_trip_size_id_by_name(trip_size_name):
    return models.TripSize.objects.all().filter(name=trip_size_name)[0].id


def get_club_id_by_name(club_name):
    result = models.Club.objects.all().filter(name=club_name)
    if result:
        return result[0].id
    else:
        return None


def get_license_instance_by_id(license_id):
    return models.License.objects.all().filter(id=license_id)[0]


def get_license_id_by_name(license_id):
    return models.License.objects.all().filter(id=license_id)[0].id


def get_club_name_by_id(club_id):
    result = models.Club.objects.filter(id=club_id)
    if result:
        return result[0].name
    return None


def get_license_name_by_id(license_id):
    result = models.License.objects.filter(id=license_id)
    if result:
        return result[0].name
    return None
