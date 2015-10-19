# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0005_auto_20151013_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='surprise',
            name='metadata_retrieved',
            field=models.DateTimeField(null=True),
        ),
    ]
