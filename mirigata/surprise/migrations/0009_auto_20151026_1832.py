# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0008_auto_20151019_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='surprise',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 18, 32, 7, 852617, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surprise',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 18, 32, 15, 156351, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
