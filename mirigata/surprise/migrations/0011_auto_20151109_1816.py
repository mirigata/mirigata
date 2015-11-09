# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('surprise', '0010_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('amount', models.SmallIntegerField(choices=[(1, 'Up'), (-1, 'Down')])),
                ('surprise', models.ForeignKey(to='surprise.Surprise')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'surprise')]),
        ),
    ]
