from django.contrib import admin
from django.contrib.auth.admin import *
from MainApp.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
