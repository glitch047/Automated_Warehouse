# Generated by Django 4.0.1 on 2024-03-08 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_request_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile'),
        ),
    ]
