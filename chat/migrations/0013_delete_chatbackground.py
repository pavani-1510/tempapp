# Generated by Django 5.0.4 on 2024-06-24 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_chatbackground'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChatBackground',
        ),
    ]