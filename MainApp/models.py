from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # vk_id is username
    # access_token = models.CharField(max_length=100, default='')

    def __init__(self):
        self.username = models.CharField(max_length=100, default='')
        self.access_token = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.username
