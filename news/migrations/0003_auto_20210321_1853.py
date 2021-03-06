# Generated by Django 2.2 on 2021-03-21 15:53

from django.db import migrations, models
import news.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20210108_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='cover',
            field=models.ImageField(blank=True, default=None, max_length=120, null=True, upload_to=news.models.get_news_cover_path),
        ),
        migrations.AlterField(
            model_name='newscontentimage',
            name='img',
            field=models.ImageField(blank=True, default=None, max_length=120, null=True, upload_to=news.models.get_news_content_image_path),
        ),
        migrations.AlterField(
            model_name='newscover',
            name='content',
            field=models.CharField(blank=True, default='', max_length=60),
        ),
    ]
