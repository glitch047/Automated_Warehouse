# Generated by Django 4.0.1 on 2024-03-08 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_manager_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='image',
        ),
    ]
