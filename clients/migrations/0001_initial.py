# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('tier', models.CharField(max_length=32)),
                ('start_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('parent_name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
            ],
        ),
    ]
