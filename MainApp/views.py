import urllib
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
# from flask import json
from MainApp.models import *

# Create your views here.


def get_access_token(request):
    client_id = '6340308'
    client_secret = 'K1umBhHtCQNdl6LW8bVk'
    redirect_uri = 'http://turmezzz.pythonanywhere.com/get_access_token'
    code = request.GET['code']
    url = f'https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}'
    access_token = json.loads(urllib.request.urlopen(url).read())
    auth.login(request, login=access_token, password='password')
    return HttpResponse(access_token)
    # return redirect('search')


def login(request):
    if request.user.is_authenticated():
        # ret = '''It's okey. Redirect to search'''
        # return HttpResponse(ret)
        return redirect('search')
        # return render(request, 'mainApp/search.html')
    else:
        user = User.objects.create(username='fucku2')
        user.set_password('fuckutwice')
        user.save()
        auth.login(request, user)
        # return HttpResponse('fuck u')
        return render(request, 'mainApp/auth.html')


def search(request):
    return render(request, 'mainApp/search.html')





