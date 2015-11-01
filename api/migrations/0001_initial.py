# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=60)),
                ('social_id', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PuzzleData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
                ('score', models.IntegerField()),
                ('stars', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='puzzle_data',
            field=models.ManyToManyField(to='api.PuzzleData'),
        ),
    ]
