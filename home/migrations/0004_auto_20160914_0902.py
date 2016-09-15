# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 09:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepagecarouselitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagecarouselitem',
            name='caption',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='homepagecarouselitem',
            name='embed_link',
            field=models.URLField(null=True, verbose_name='Embed URL'),
        ),
    ]
