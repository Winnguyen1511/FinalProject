# Generated by Django 3.0.6 on 2020-07-01 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglotmanager', '0002_auto_20200701_0649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cameralist',
            options={'managed': False, 'permissions': [('edit_cameralist', 'Can edit camera list')]},
        ),
    ]
