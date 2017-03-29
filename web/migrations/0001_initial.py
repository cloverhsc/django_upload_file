# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=64)),
                ('author', models.CharField(max_length=128)),
                ('md5', models.CharField(max_length=64)),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['title'],
                'db_table': 'Book',
            },
        ),
    ]
