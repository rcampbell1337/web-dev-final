# Generated by Django 3.2.2 on 2021-06-08 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='last_name_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
