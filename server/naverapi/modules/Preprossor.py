from django.http import HttpResponse
import requests, json
from django.conf import settings
import pickle

def preprosessor(request):
    fopen = open(r'C:\Users\user\Desktop\data.txt', 'r')
    i=0
    temp_list=[]
    line = fopen.readlines()
    while True:
        print(i)

        if not line: break
        client_id = getattr(settings, 'NAVER_ID')
        client_secret = getattr(settings, 'NAVER_SECRET')
        url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
        header = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/json"
        }
        data = {
            'content': line[7001+i]
        }
        r = requests.post(url, data=json.dumps(data), headers=header)
        k = HttpResponse(r)
        temp_list.append(k.getvalue().decode('utf-8'))
        i+=1
        if i==133 or 7000+i==len(temp_list)-2:
            print(temp_list[-1])
            break
    fopen.close()
    with  open(r"C:\Users\user\Desktop\data24.pickle",'wb') as fs:
        pickle.dump(temp_list, fs)
    # 처리결과 리턴 필요(not RESPONSE)
    return HttpResponse(i)

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
        'content': "싸늘하다. 가슴에 비수가 날아와 꽂힌다." #request 값으로 변경 예정
    }
    r = requests.post(url, data=json.dumps(data), headers=header)

    return HttpResponse(r)
