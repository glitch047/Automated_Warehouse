# Generated by Django 4.0.1 on 2024-03-06 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_alter_vendorrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
