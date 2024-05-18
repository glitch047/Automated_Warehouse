# Generated by Django 4.0.1 on 2024-03-09 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_remove_manager_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDeleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('batchno', models.BigIntegerField()),
                ('productno', models.BigIntegerField()),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('batchno', models.BigIntegerField()),
                ('productno', models.BigIntegerField()),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
