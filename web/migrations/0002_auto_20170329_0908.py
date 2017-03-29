# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.CharField(max_length=50, unique=True, serialize=False, primary_key=True)),
                ('auth_type', models.IntegerField(default=0, choices=[(0, b'None'), (1, b'Plain'), (2, b'MD5'), (3, b'SHA1')])),
                ('version', models.CharField(max_length=250)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
