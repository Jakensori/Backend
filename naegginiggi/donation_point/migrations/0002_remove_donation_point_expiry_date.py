# Generated by Django 4.1.6 on 2023-03-29 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation_point', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation_point',
            name='expiry_date',
        ),
    ]
