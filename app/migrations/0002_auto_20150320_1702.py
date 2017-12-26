# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='munchedfeedcache',
            name='id',
        ),
        migrations.AlterField(
            model_name='munchedfeedcache',
            name='munched_feed',
            field=models.OneToOneField(primary_key=True, serialize=False, to='app.MunchedFeed', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
