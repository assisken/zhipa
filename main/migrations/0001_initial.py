# Generated by Django 2.2 on 2019-06-18 23:54

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('schedule', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(blank=True, default='', max_length=60)),
                ('img', models.ImageField(blank=True, default='', max_length=120, upload_to='')),
                ('description', models.TextField()),
                ('text', models.TextField()),
                ('hidden', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=30)),
                ('firstname', models.CharField(max_length=30)),
                ('middlename', models.CharField(max_length=30)),
                ('img', models.ImageField(blank=True, default=None, max_length=60, null=True, upload_to='images/lecturers')),
                ('regalia', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('leader', models.BooleanField(default=False)),
                ('lecturer', models.BooleanField(default=True)),
                ('hide', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Staff',
                'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('leader'), descending=True), django.db.models.expressions.OrderBy(django.db.models.expressions.F('lecturer'), descending=True), django.db.models.expressions.OrderBy(django.db.models.expressions.F('hide')), django.db.models.expressions.OrderBy(django.db.models.expressions.F('lastname')), django.db.models.expressions.OrderBy(django.db.models.expressions.F('firstname')), django.db.models.expressions.OrderBy(django.db.models.expressions.F('middlename')), django.db.models.expressions.OrderBy(django.db.models.expressions.F('pk'))],
            },
        ),
    ]
