# Generated by Django 4.0.1 on 2024-03-05 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_product_batchno_alter_product_productno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='manager',
        ),
    ]
