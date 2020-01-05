# Generated by Django 2.2.6 on 2019-11-24 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chandeleur_app', '0002_registeredperson_user_in_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredperson',
            name='user_in_charge',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]