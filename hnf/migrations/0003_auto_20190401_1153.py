# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-01 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hnf', '0002_auto_20190329_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='other',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='return_time',
            field=models.DateTimeField(max_length=32, null=True, verbose_name=b'\xe5\xbd\x92\xe8\xbf\x98\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
