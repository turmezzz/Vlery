import urllib
import json
import vk


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from MainApp.models import User
from . import tools

# Create your views here.


def get_access_token(request):
    client_id = '6340308'
    client_secret = 'K1umBhHtCQNdl6LW8bVk'
    redirect_uri = 'http://turmezzz.pythonanywhere.com/get_access_token'
    code = request.GET['code']
    url = f'https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}'
    data = json.loads(urllib.request.urlopen(url).read())
    access_token = data['access_token']
    vk_id = data['user_id']

    user = auth.authenticate(username=vk_id, password='password')
    if user is None or user.is_anonymous():
        user = User.objects.create(username=vk_id, access_token=access_token)
        user.set_password('password')
        user.save()
        auth.login(request, user)
        tool = tools.Tool(request)
        tool.create_new_account()
        auth.authenticate(username=vk_id, password='password')
    else:
        user = User.objects.get(username=vk_id)
        user.access_token = access_token
        user.save()
        auth.login(request, user)
        tool = tools.Tool(request)
        tool.update_posts()
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
    tool.update_posts()
    img_url = tool.get_img_url()
    name = tool.get_name()

    data = {'img_url': img_url, 'name': name}
    return render(request, 'MainApp/home.html', data)


def search(request):
    if not request.user.is_authenticated():
        return redirect('login')

    # Здесь не происходит обновления постов

    if request.method == 'POST':
        q = request.POST['q']
        tool = tools.Tool(request)
        posts = tools.search(request.user, q)
        img_url = tool.get_img_url()
        data = {'queue': q, 'img_url': img_url, 'posts': posts}
        return render(request, 'MainApp/output.html', data)










