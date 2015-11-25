# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0010_auto_20151110_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='switchport',
            name='vf_vsan',
        ),
        migrations.AddField(
            model_name='switch',
            name='vf_vsan',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='password',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='vendor',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='switchport',
            name='port_index',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
