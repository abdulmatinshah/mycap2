# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-17 18:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_auto_20160917_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageb',
            name='imagee',
        ),
        migrations.RemoveField(
            model_name='imagegallery',
            name='imageb_ptr',
        ),
        migrations.RemoveField(
            model_name='imagegallery',
            name='page',
        ),
        migrations.DeleteModel(
            name='ImageB',
        ),
        migrations.DeleteModel(
            name='ImageGallery',
        ),
    ]
