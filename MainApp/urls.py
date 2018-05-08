from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^get_access_token', views.get_access_token, name='get_access_token'),
    url(r'^home', views.home, name='home'),
    url(r'^search', views.search, name='search'),

]
