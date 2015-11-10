# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0009_auto_20151110_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hbaport',
            name='link_down',
            field=models.NullBooleanField(),
        ),
    ]
