# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('nt_account', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('host_name', models.CharField(max_length=20)),
                ('ip_addr', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(to='forests.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='team',
            field=models.ForeignKey(to='forests.Team'),
        ),
        migrations.AddField(
            model_name='employee',
            name='team',
            field=models.ForeignKey(to='forests.Team'),
        ),
    ]
