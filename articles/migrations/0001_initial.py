# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mycap.util_streamfield
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.CharField(max_length=250, null=True)),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(classname='full', icon='pilcrow')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.TextBlock('Quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock())))), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', mycap.util_streamfield.ImageAlignmentChoiceBlock())), icon='image', label='Aligned image')), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', mycap.util_streamfield.HtmlAlignedFieldBlock())), icon='pilcrow', label='Aligned html')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]