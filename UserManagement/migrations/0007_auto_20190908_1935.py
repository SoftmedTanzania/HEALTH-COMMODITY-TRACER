# Generated by Django 2.1.3 on 2019-09-08 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0006_auto_20190729_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MasterDataManagement.Location'),
        ),
    ]
