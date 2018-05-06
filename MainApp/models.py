from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    def __init(self):
        # vk_id is username
        self.access_token = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.username
