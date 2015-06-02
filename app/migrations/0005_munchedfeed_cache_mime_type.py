# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150406_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='munchedfeed',
            name='cache_mime_type',
            field=models.TextField(null=True),
        ),
    ]
