# Generated by Django 5.0.7 on 2024-07-16 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bids'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bids',
            new_name='Bid',
        ),
    ]
