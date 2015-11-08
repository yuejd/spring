# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0006_auto_20151102_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='owner',
            field=models.ForeignKey(to='forests.Employee', null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='team',
            field=models.ForeignKey(to='forests.Team', null=True),
        ),
    ]
