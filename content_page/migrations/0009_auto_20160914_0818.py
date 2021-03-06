# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('wagtaildocs', '0007_merge'),
        ('content_page', '0008_auto_20160914_0808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentpagecarouselitem',
            name='linkfields_ptr',
        ),
        migrations.AddField(
            model_name='contentpagecarouselitem',
            name='document_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.Document'),
        ),
        migrations.AddField(
            model_name='contentpagecarouselitem',
            name='external_link',
            field=models.URLField(default=1, verbose_name='External url'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contentpagecarouselitem',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contentpagecarouselitem',
            name='page_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
        migrations.DeleteModel(
            name='LinkFields',
        ),
    ]
