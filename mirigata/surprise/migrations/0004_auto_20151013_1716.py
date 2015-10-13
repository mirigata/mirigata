# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0003_surprise_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='surprise',
            name='title',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='surprise',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
    ]
