# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0006_surprise_metadata_retrieved'),
    ]

    operations = [
        migrations.AddField(
            model_name='surprise',
            name='link_exists',
            field=models.BooleanField(default=True),
        ),
    ]
