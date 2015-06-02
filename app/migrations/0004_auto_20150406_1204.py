# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20150405_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='munchedfeed',
            name='content_regex',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='munchedfeed',
            name='extract_css_selector',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='munchedfeed',
            name='title_regex',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
