# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


SURPRISES = (
    dict(
        id='7SJryrDxcckECCQ22TdaDW',
        link='http://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/',
        description='PHP, a fractal of bad design',
    ),
    dict(
        id='g7PdQxpuUv4pMTRR83dKzg',
        link='http://beej.us/guide/bgnet/output/html/singlepage/bgnet.html',
        description="Beej's guide to network programming",
    ),
    dict(
        id='V7DahRTsqHzLwgUv8bnyhV',
        link='http://www.godutch.com/newspaper/index.php?id=212',
        description='The Mother of America (spoiler: the Dutch)',
    ),
    dict(
        id='DXKeEqQZLU9QWmREfE8gCm',
        link='http://medievalbooks.nl/2015/09/04/medieval-posters/',
        description='Medieval Posters',
    ),
)


def create_surprises(apps, schema_editor):
    Surprise = apps.get_model('surprise', 'Surprise')
    for s in SURPRISES:
        Surprise.objects.create(
            id=s['id'],
            link=s['link'],
            description=s['description']
        )


def remove_surprises(apps, schema_editor):
    Surprise = apps.get_model('surprise', 'Surprise')
    for s in SURPRISES:
        Surprise.objects.get(pk=s['id']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('surprise', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=create_surprises,
            reverse_code=remove_surprises,
        )
    ]
