# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0013_make_rendition_upload_callable'),
        ('articles', '0002_auto_20160914_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('imagelink_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='articles.ImageLink')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_gallery', to='articles.ArticlePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=('articles.imagelink', models.Model),
        ),
        migrations.AddField(
            model_name='imagelink',
            name='imagelink',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
