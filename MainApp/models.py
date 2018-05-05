from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # access_token is saved in username as login of account
    # access_token = models.CharField(max_length=30, default='')
    vk_id = models.IntegerField(default=-1)

    def __str__(self):
        return self.username
