# Generated by Django 3.2.11 on 2022-05-09 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220509_2126'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AboutManager',
            new_name='About',
        ),
    ]