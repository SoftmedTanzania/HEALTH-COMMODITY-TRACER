# Generated by Django 2.1.3 on 2019-07-29 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0005_auto_20190718_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='dev_id',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
    ]
