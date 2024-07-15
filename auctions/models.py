from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    starting_bid = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
