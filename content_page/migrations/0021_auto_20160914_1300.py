# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 13:00
from __future__ import unicode_literals

import content_page.models
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('content_page', '0020_auto_20160914_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('h1', wagtail.wagtailcore.blocks.CharBlock(icon='title')), ('h2', wagtail.wagtailcore.blocks.CharBlock(icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(classname='full', icon='pilcrow')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.TextBlock('Quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock())))), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', content_page.models.ImageAlignmentChoiceBlock())), icon='image', label='Aligned image')), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', content_page.models.HtmlAlignedFieldBlock())), icon='pilcrow', label='Aligned html')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))), blank=True, null=True),
        ),
    ]