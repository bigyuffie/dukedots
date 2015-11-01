# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='puzzledata',
            old_name='level',
            new_name='puzzles',
        ),
        migrations.RenameField(
            model_name='puzzledata',
            old_name='score',
            new_name='scores',
        ),
    ]
