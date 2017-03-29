# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20170329_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('md5', models.CharField(max_length=128, unique=True, serialize=False, primary_key=True)),
                ('fw', models.FileField(upload_to=web.models.generate_fw_path)),
                ('size', models.IntegerField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]
