from .modules.Preprossor import preprosessor, sentiment_analysis
from .tasks import sentiment_analysis
from django.http import HttpResponse
from django.conf import settings
import json, requests
from django.core.files.storage import default_storage

# Create your views here.
# Preprosessing
def index(request):
    client_id = getattr(settings, 'NAVER_ID')
    client_secret = getattr(settings, 'NAVER_SECRET')
    input = json.loads(request.body)
    url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
    header = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret,
        "Content-Type": "application/json"
    }
    data = {
        'content': input['dialog']  # request 값으로 변경 예정
    }
    r = requests.post(url, data=json.dumps(data), headers=header)
    k = HttpResponse(r)
    temp = [k.getvalue().decode('utf-8')]
    sentiment_analysis.delay(temp, input['deviceId'])
    return HttpResponse("Completed")

def index2(request):
    result = preprosessor(request)
    return result