from django.shortcuts import render
from django.http import HttpResponse
import time
import requests, json
from django.conf import settings

def service(request):
    client_id = getattr(settings, 'NAVER_ID')
    client_secret = getattr(settings, 'NAVER_SECRET')
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    header = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    data = {
        'content': "싸늘하다. 가슴에 비수가 날아와 꽂힌다."
    }
    r = requests.post(url, data=json.dumps(data), headers=header)
    return HttpResponse(r)