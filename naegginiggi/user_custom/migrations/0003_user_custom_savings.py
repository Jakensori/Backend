# Generated by Django 4.1.6 on 2023-05-21 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_custom', '0002_user_custom_authority'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_custom',
            name='savings',
            field=models.IntegerField(default=0),
        ),
    ]