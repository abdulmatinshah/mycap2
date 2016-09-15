# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 12:13
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content_page', '0013_auto_20160914_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.TextBlock('Quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock())))),), null=True),
        ),
    ]
