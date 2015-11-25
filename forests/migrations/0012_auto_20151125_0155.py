# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0011_auto_20151118_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hba',
            name='model',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='hba',
            name='serial_number',
            field=models.CharField(null=True, max_length=50),
        ),
    ]
