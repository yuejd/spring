# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HBA',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('vendor', models.CharField(max_length=20)),
                ('wwn', models.CharField(max_length=23)),
                ('model', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='HbaPort',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('wwn', models.CharField(max_length=23)),
                ('link_down', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('vendor', models.CharField(max_length=20)),
                ('ip_addr', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SwitchPort',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('port_index', models.IntegerField()),
                ('vf_vsan', models.IntegerField()),
                ('switch', models.ForeignKey(to='forests.Switch')),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='os',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='hbaport',
            name='connection',
            field=models.ForeignKey(to='forests.SwitchPort'),
        ),
        migrations.AddField(
            model_name='hbaport',
            name='hba_card',
            field=models.ForeignKey(to='forests.HBA'),
        ),
    ]
