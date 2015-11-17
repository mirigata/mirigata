# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
from django.conf import settings
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('surprise', '0013_auto_20151110_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', shortuuidfield.fields.ShortUUIDField(max_length=22, serialize=False, primary_key=True, editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, related_name='children', to='surprise.Comment', null=True)),
                ('surprise', models.ForeignKey(related_name='comments', to='surprise.Surprise')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
