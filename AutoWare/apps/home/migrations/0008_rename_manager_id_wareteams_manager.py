# Generated by Django 4.0.1 on 2024-03-02 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_wareteams_manager_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wareteams',
            old_name='manager_id',
            new_name='manager',
        ),
    ]
