import urllib
import json
import vk


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from MainApp.models import *
from . import tools

# Create your views here.


def get_access_token(request):
    client_id = '6340308'
    client_secret = 'K1umBhHtCQNdl6LW8bVk'
    redirect_uri = 'http://turmezzz.pythonanywhere.com/get_access_token'
    # redirect_uri = 'blank.html'
    code = request.GET['code']
    url = f'https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}'
    data = json.loads(urllib.request.urlopen(url).read())
    access_token = data['access_token']
    vk_id = data['user_id']
    return HttpResponse(str(access_token) + ' ' + str(vk_id))



    user = User.objects.create(username=access_token, vk_id=vk_id)
    user.set_password('password')
    user.save()
    auth.authenticate(username=access_token, password='password')
    auth.login(request, user)
    return redirect('home')


def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        return render(request, 'MainApp/auth.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def home(request):
    if not request.user.is_authenticated():
        return redirect('login')

    tool = tools.Tool(request)
    # img_url = tool.get_img_url()
    name = tool.get_name()
    img_url = ''

    data = {'img_url': img_url, 'name': name}
    return render(request, 'MainApp/home.html', data)






