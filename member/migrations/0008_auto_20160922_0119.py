# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 01:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_auto_20160917_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberpage',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='memberpage',
            name='last_name',
        ),
    ]