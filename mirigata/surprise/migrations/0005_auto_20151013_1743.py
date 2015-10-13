# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0004_auto_20151013_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='surprise',
            name='author_name',
            field=models.TextField(max_length=500, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='surprise',
            name='thumbnail_url',
            field=models.URLField(max_length=500, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='surprise',
            name='title',
            field=models.TextField(max_length=500, blank=True, null=True),
        ),
    ]
