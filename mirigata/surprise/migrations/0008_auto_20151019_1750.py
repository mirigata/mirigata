# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0007_surprise_link_exists'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surprise',
            name='link_exists',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
