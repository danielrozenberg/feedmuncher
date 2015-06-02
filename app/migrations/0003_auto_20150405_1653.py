# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150320_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='munchedfeedcache',
            name='munched_feed',
        ),
        migrations.AddField(
            model_name='munchedfeed',
            name='cache',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='munchedfeed',
            name='last_updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.DeleteModel(
            name='MunchedFeedCache',
        ),
    ]
