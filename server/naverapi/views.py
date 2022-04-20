from django.shortcuts import render
from django.http import HttpResponse
import time
import requests, json
from django.conf import settings
from server.naverapi.modules.Preprossor import preprosessor
from server.naverapi.modules.service import service

# Create your views here.
# Preprosessing
def index(request):
    result = service(request)
    return result