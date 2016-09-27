# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 06:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0005_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='search_engine.Site'),
        ),
    ]