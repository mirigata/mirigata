# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surprise', '0012_auto_20151109_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 11, 10, 18, 30, 47, 909194, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vote',
            name='surprise',
            field=models.ForeignKey(related_name='votes', to='surprise.Surprise'),
        ),
    ]
