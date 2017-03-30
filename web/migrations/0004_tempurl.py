# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempUrl',
            fields=[
                ('url_token', models.CharField(max_length=128, unique=True, serialize=False, primary_key=True)),
                ('expire_time', models.DateTimeField(blank=True)),
                ('target_file', models.ForeignKey(to='web.Files')),
            ],
            options={
                'db_table': 'TempUrl',
            },
        ),
    ]
