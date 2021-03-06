# Generated by Django 2.1.3 on 2019-08-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MasterDataManagement', '0011_auto_20190805_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthcommoditybalance',
            name='status',
        ),
        migrations.AddField(
            model_name='healthcommoditiescategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='healthcommodity',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='healthcommoditybalance',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='healthcommoditytransactions',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='location',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='postingfrequency',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='postingschedule',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
