# Generated by Django 4.2.5 on 2023-09-14 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_rename_path_chrome_pc_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cookie',
            name='creation_time',
        ),
    ]
