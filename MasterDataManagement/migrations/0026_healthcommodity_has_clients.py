# Generated by Django 2.1.3 on 2019-12-20 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MasterDataManagement', '0025_auto_20191022_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcommodity',
            name='has_clients',
            field=models.BooleanField(default=False),
        ),
    ]
