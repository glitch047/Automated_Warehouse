# Generated by Django 4.0.1 on 2024-03-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_vendorrequest_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorrequest',
            name='status',
            field=models.PositiveIntegerField(default=2),
        ),
    ]