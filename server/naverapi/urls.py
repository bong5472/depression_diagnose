from django.urls import path

from . import views

urlpatterns = [
    path('preprosess', views.index, name='index'),
    path('naverapi', views.index2, name='index'),
]