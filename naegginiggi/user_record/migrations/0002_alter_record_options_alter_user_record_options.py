# Generated by Django 4.1.6 on 2023-03-04 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_record', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='user_record',
            options={'managed': False},
        ),
    ]
