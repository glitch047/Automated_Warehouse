# Generated by Django 4.0.1 on 2024-03-03 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='batchno',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='productno',
            field=models.BigIntegerField(),
        ),
    ]
