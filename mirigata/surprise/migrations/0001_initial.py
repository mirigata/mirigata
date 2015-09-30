# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Surprise',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(serialize=False, primary_key=True, editable=False, max_length=22, blank=True)),
                ('link', models.URLField(max_length=500)),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
    ]
