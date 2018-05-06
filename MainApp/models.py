from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # vk_id is username
    access_token = models.IntegerField(default=-1)

    def __str__(self):
        return self.username
