from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='index'),
    path('login', views.login, name='index'),
    path('giveData', views.giveData, name='index'),
]