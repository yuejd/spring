# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0005_remove_switch_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hbaport',
            name='updated',
        ),
        migrations.AddField(
            model_name='server',
            name='updated',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
