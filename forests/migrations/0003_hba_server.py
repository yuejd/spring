# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0002_auto_20151019_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='hba',
            name='server',
            field=models.ForeignKey(default=None, to='forests.Server'),
        ),
    ]
