# Generated by Django 4.2.7 on 2024-11-22 17:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0006_alter_ad_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='favourites',
        ),
        migrations.AddField(
            model_name='ad',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_ads', through='ads.Fav', to=settings.AUTH_USER_MODEL),
        ),
    ]
