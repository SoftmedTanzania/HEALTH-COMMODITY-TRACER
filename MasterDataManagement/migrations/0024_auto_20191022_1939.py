# Generated by Django 2.1.3 on 2019-10-22 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MasterDataManagement', '0023_auto_20191022_1621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='healthcommodity',
            old_name='elmis_product_id',
            new_name='elims_product_id',
        ),
    ]
