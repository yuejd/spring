# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0008_auto_20151108_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hbaport',
            old_name='wwn',
            new_name='wwpn',
        ),
        migrations.RemoveField(
            model_name='hba',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='hba',
            name='wwn',
        ),
        migrations.AddField(
            model_name='hba',
            name='description',
            field=models.CharField(null=True, max_length=200),
        ),
        migrations.AddField(
            model_name='hba',
            name='driver_name',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AddField(
            model_name='hba',
            name='driver_version',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AddField(
            model_name='hba',
            name='firmware_version',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AddField(
            model_name='hba',
            name='serial_number',
            field=models.CharField(default='1111', max_length=50),
            preserve_default=False,
        ),
    ]
