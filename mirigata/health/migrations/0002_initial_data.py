# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_healthcheck_data(apps, schema_editor):
    HealthCheck = apps.get_model('health', 'HealthCheck')
    HealthCheck.objects.create()


def remove_healthcheck_data(apps, schema_editor):
    HealthCheck = apps.get_model('health', 'HealthCheck')
    HealthCheck.objects.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=create_healthcheck_data,
            reverse_code=remove_healthcheck_data,
        )
    ]
