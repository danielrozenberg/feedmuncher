# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_munchedfeed_cache_mime_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='munchedfeed',
            name='cache',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='munchedfeed',
            name='cache_mime_type',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='munchedfeed',
            name='last_updated',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
