# Generated by Django 5.0.7 on 2024-07-15 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_category_alter_listing_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner_id',
            field=models.IntegerField(blank=True, default=False),
        ),
    ]
