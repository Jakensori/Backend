# Generated by Django 4.1.6 on 2023-03-20 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_user_campaign_donation_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='image',
            field=models.CharField(max_length=200),
        ),
    ]