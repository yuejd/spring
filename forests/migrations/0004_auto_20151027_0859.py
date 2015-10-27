# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0003_hba_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hbaport',
            name='connection',
            field=models.ForeignKey(to='forests.SwitchPort', null=True),
        ),
    ]
