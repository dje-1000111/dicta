# Generated by Django 5.0 on 2024-01-25 01:24

import apps.dictation.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(blank=True, max_length=50, null=True)),
                ('filename', models.CharField(blank=True, max_length=200, null=True)),
                ('timestamps', models.JSONField()),
                ('topic', models.CharField(max_length=200)),
                ('level', models.IntegerField()),
                ('tip', models.JSONField()),
                ('slug', models.SlugField(default='')),
                ('total_line', models.IntegerField(default=0)),
                ('in_production', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Practice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_current_line', models.IntegerField(blank=True, null=True)),
                ('lines', models.JSONField(default=apps.dictation.models.lines_default)),
                ('user_rating', models.CharField(blank=True, max_length=1, null=True)),
                ('is_done', models.BooleanField(default=False, verbose_name='is_dictation_done')),
                ('dictation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictation.dictation')),
            ],
        ),
    ]
