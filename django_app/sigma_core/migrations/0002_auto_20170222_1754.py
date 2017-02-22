# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-22 16:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sigma_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sigma_core.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sigma_core.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sigma_core.Publication')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='school', to='sigma_core.Group'),
        ),
        migrations.AddField(
            model_name='tag',
            name='tagged',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
