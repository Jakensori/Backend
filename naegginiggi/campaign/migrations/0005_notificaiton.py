# Generated by Django 4.1.6 on 2023-05-24 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_remove_review_campaign_delete_message_delete_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificaiton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('foundation', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('image', models.CharField(max_length=200)),
                ('camapaign', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='campaign.campaign')),
            ],
            options={
                'db_table': 'Notification',
                'managed': True,
            },
        ),
    ]
