# Generated by Django 4.2.7 on 2024-11-20 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ads', '0004_comment_ad_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fav',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads.ad')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favs_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('ad', 'user')},
            },
        ),
        migrations.AddField(
            model_name='ad',
            name='favourites',
            field=models.ManyToManyField(related_name='favourite_ads', through='ads.Fav', to=settings.AUTH_USER_MODEL),
        ),
    ]
