# Generated by Django 3.2.9 on 2024-06-07 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20240606_2029'),
    ]

    operations = [
        migrations.DeleteModel(
            name='File',
        ),
        migrations.RenameField(
            model_name='attempts',
            old_name='attempt',
            new_name='Attempt',
        ),
    ]
