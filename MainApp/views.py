import urllib
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from MainApp.models import *

# Create your views here.


def get_access_token(request):
    client_id = '6340308'
    client_secret = 'K1umBhHtCQNdl6LW8bVk'
    redirect_uri = 'http://turmezzz.pythonanywhere.com/get_access_token'
    code = request.GET['code']
    url = f'https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}'
    data = json.loads(urllib.request.urlopen(url).read())
    access_token = data['access_token']
    user = User.objects.create(username=access_token)
    user.set_password('password')
    user.save()
    auth.authenticate(username=access_token, password='password')
    auth.login(request, user)
    return redirect('search')



def login(request):
    if request.user.is_authenticated():
        return redirect('search')
    else:
        return render(request, 'MainApp/auth.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def search(request):
    if not request.user.is_authenticated():
        return redirect('login')

    img_url = 'https://pp.userapi.com/c637117/v637117242/5b3ac/pBlG-5UZScc.jpg'
    name = request.user.username
    data = {'img_url': img_url, 'name': name}

    return render(request, 'MainApp/search.html', data)





