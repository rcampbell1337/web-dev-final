# Generated by Django 3.2.2 on 2021-06-09 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userbase_last_name_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbase',
            old_name='last_name_name',
            new_name='last_name',
        ),
    ]
