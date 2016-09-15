# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_page', '0010_auto_20160914_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpagecarouselitem',
            name='caption',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='contentpagecarouselitem',
            name='embed_link',
            field=models.URLField(blank=True, null=True, verbose_name='Embed URL'),
        ),
    ]
