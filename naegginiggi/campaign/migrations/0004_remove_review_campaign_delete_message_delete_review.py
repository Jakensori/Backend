# Generated by Django 4.1.6 on 2023-05-23 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0003_alter_campaign_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
