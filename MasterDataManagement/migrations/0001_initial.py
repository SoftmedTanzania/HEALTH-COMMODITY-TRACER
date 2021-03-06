# Generated by Django 2.1.3 on 2019-07-17 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_type_description', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'HCT_FacilityTypes',
            },
        ),
        migrations.CreateModel(
            name='HealthCommoditiesCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_commodity_category_name', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'HCT_HealthCommoditiesCategories',
            },
        ),
        migrations.CreateModel(
            name='HealthCommodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_commodity_name', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('track_number_of_patients', models.BooleanField(default=False)),
                ('track_wastage', models.BooleanField(default=False)),
                ('track_quantity_expired', models.BooleanField(default=False)),
                ('health_commodity_category', models.ForeignKey(blank=True, null=True, on_delete=
                django.db.models.deletion.SET_NULL, to='MasterDataManagement.HealthCommoditiesCategory')),
            ],
            options={
                'db_table': 'HCT_HealthCommodities',
            },
        ),
        migrations.CreateModel(
            name='HealthCommodityBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_available', models.IntegerField(blank=True, null=True)),
                ('quantity_consumed', models.IntegerField(blank=True, default=0, null=True)),
                ('health_commodity', models.ForeignKey(on_delete=
                                                       django.db.models.deletion.CASCADE, to='MasterDataManagement.HealthCommodity')),
            ],
            options={
                'db_table': 'HCT_HealthCommodityBalance',
            },
        ),
        migrations.CreateModel(
            name='HealthCommodityTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_created', models.DateTimeField(auto_now=True)),
                ('trans_date_time', models.BigIntegerField()),
                ('quantity_available', models.IntegerField()),
                ('quantity_consumed', models.IntegerField()),
                ('has_patients', models.BooleanField()),
                ('stock_out_days', models.IntegerField(blank=True, null=True)),
                ('quantity_wasted', models.IntegerField(blank=True, null=True)),
                ('quantity_expired', models.IntegerField(blank=True, null=True)),
                ('number_of_clients', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'HCT_HealthCommodityTransactions',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elims_facility_id', models.IntegerField(blank=True, null=True)),
                ('location_type', models.CharField(choices=[('CTRY', 'country'), ('RGN', 'region'),
                                                            ('DST', 'district'), ('FCT', 'facility')], max_length=25)),
                ('location_name', models.CharField(max_length=255)),
                ('coordinates', models.CharField(blank=True, max_length=150, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('facility_type', models.ForeignKey(blank=True, null=True, on_delete=
                django.db.models.deletion.SET_NULL, to='MasterDataManagement.FacilityType')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=
                django.db.models.deletion.SET_NULL, related_name='children', to='MasterDataManagement.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_created', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=150)),
                ('message_body', models.TextField()),
                ('parent_message_id', models.IntegerField(blank=True, default=0, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'HCT_Messages',
            },
        ),
        migrations.CreateModel(
            name='MessageRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('is_trashed', models.BooleanField(default=False)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='MasterDataManagement.Location')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              to='MasterDataManagement.Message')),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'HCT_MessageRecipients',
            },
        ),
        migrations.CreateModel(
            name='PostingFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency_description', models.CharField(max_length=150)),
                ('number_of_days', models.IntegerField()),
            ],
            options={
                'db_table': 'HCT_PostingFrequencies',
            },
        ),
        migrations.CreateModel(
            name='PostingSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField()),
                ('status', models.CharField(default='pending', max_length=100)),
                ('health_commodity_balance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                               to='MasterDataManagement.HealthCommodityBalance')),
            ],
            options={
                'db_table': 'HCT_PostingSchedule',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=30)),
                ('unit_description', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'HCT_Units',
            },
        ),
        migrations.AddField(
            model_name='healthcommoditytransactions',
            name='posting_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='MasterDataManagement.PostingSchedule'),
        ),
        migrations.AddField(
            model_name='healthcommoditytransactions',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='healthcommoditybalance',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MasterDataManagement.Location'),
        ),
        migrations.AddField(
            model_name='healthcommoditybalance',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='healthcommodity',
            name='posting_frequency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='MasterDataManagement.PostingFrequency'),
        ),
        migrations.AddField(
            model_name='healthcommodity',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='MasterDataManagement.Unit'),
        ),
    ]
