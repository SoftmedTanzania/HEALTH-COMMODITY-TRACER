# Generated by Django 2.1.3 on 2019-08-05 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MasterDataManagement', '0012_auto_20190805_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcommodity',
            name='elmis_product_code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
