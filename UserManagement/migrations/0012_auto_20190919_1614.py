# Generated by Django 2.1.3 on 2019-09-19 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0011_facilitysettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facilitysettings',
            name='facility_id',
        ),
        migrations.DeleteModel(
            name='FacilitySettings',
        ),
    ]
