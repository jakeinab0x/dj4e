# Generated by Django 4.2.7 on 2024-08-20 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ad',
            old_name='update_at',
            new_name='updated_at',
        ),
    ]
