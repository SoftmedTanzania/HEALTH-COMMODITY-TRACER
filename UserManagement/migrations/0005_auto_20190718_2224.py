# Generated by Django 2.1.3 on 2019-07-18 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0004_auto_20190717_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reg_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
