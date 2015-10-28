# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0008_auto_20151019_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='surprise',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
