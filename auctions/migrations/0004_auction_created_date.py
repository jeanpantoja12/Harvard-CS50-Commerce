# Generated by Django 3.0.4 on 2021-03-19 22:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
