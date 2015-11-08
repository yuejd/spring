# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0007_auto_20151108_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='host_name',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='server',
            name='os',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
