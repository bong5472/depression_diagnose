from django.http import HttpResponse
import requests, json
from django.conf import settings
import pickle
import service
def preprosessor(request):
    service.excel_to_txt()
    fopen = open(r'.\asset\data.txt', 'r')
    i=0
    temp_list=[]
    line = fopen.readlines()
    while True:
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
            'content': line[i]
        }
        r = requests.post(url, data=json.dumps(data), headers=header)
        k = HttpResponse(r)
        temp_list.append(k.getvalue().decode('utf-8'))
        i+=1
        if i==len(temp_list)-2:
            print(temp_list[-1])
            break
    fopen.close()
    with  open(r".\asset\clova_data_dump.pickle",'wb') as fs:
        pickle.dump(temp_list, fs)
    service.pickle_find_highlight()
    df=pd.read_pickle(r'.\asset\final_data_pickle')
    service.all_new_weight(df)
    return HttpResponse(i)

def sentiment_analysis(request):
    client_id = getattr(settings, 'NAVER_ID')
    client_secret = getattr(settings, 'NAVER_SECRET')
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    header = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    data = {
        'content': request.body #request 값으로 변경 예정
    }
    r = requests.post(url, data=json.dumps(data), headers=header)
    k = HttpResponse(r)
    temp=[k.getvalue().decode('utf-8')]
    with  open(r".\asset\clova_data_dump.pickle",'wb') as fs:
        pickle.dump(temp, fs)
    service.pickle_find_highlight()
    df=pd.read_pickle(r'.\asset\score.pickle')

    return HttpResponse(r)
