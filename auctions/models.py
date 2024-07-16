from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    starting_bid = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    winner_id = models.ForeignKey(User, blank=True,null=True, related_name="winner", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=30,blank=True)
    current_bid = models.IntegerField(default=False)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.FloatField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)