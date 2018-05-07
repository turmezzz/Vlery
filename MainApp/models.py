from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # vk_id is username
    access_token = models.CharField(max_length=100, default='')
    posts = models.CharField(max_length=1000 * 1000, default='')


class Post(models.Model):
    owner_id = models.CharField(max_length=100, default='')
    attachments = models.CharField(max_length=1000 * 1000, default='')
    comments = models.CharField(max_length=1000 * 1000, default='')
    id = models.CharField(max_length=100, default='')
    text = models.CharField(max_length=1000 * 1000, default='')
    link = models.CharField(max_length=100, default='')





