from django.shortcuts import render
from django.http import HttpResponse
import time
import requests, json
from django.conf import settings

# Create your views here.
def index(request):
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
    # fopen = open(r'C:\Users\user\Desktop\emotion_data\data.txt', 'r')
    # fopen1 = open(r'C:\Users\user\Desktop\emotion_data\test.txt', 'a')
    # i=0
    # while True:
    #     line = fopen.readline()
    #     if not line: break
    #
    #     client_id = getattr(settings, 'NAVER_ID')
    #     client_secret = getattr(settings, 'NAVER_SECRET')
    #     url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    #     header = {
    #         "X-NCP-APIGW-API-KEY-ID": client_id,
    #         "X-NCP-APIGW-API-KEY": client_secret,
    #         "Content-Type": "application/json"
    #     }
    #     data = {
    #         'content': line
    #     }
    #     r = requests.post(url, data=json.dumps(data), headers=header)
    #     k = HttpResponse(r)
    #     fopen1.write(k.getvalue().decode('utf-8'))
    #     time.sleep(5)
    #     i+=1
    # fopen.close()
    # fopen1.close()
    # return HttpResponse(i)