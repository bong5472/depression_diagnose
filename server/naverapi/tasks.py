import requests, json
from django.conf import settings
import pickle
from .modules import service
import pandas as pd
import os
from celery import shared_task
from .models import Log

@shared_task
def sentiment_analysis(temp, deviceId):
    currentPath = os.getcwd()
    if 'negative' not in temp[0].split(":")[2]:
        return 0
    pathname = os.path.join(currentPath, "naverapi", "modules", "asset", "clova_data_dump.pickle")
    print(temp)
    with open(pathname, 'wb') as fs:
        pickle.dump(temp, fs)
    service.pickle_find_highlight()
    df1=pd.read_pickle(currentPath + r'\naverapi\modules\asset\score_data.pickle')
    df2 =pd.read_pickle(currentPath + r'\naverapi\modules\asset\final_data.pickle')
    df3 = pd.read_pickle(currentPath + r'\naverapi\modules\asset\select_data.pickle')
    point = []
    rematch = []
    for i in df2.index:
        for k in df3.index:
            if i==k and df1.loc[k]['품사']==df3.iloc[k,2]:
                point.append(df3.iloc[k,4])
                break
    point=[]
    rematch=[]
    for i in df2.index:
        for k in df1.index:
            if i == k and df1.loc[k]['품사'] == df2.loc[i]['품사']:
                rematch.append([i, df1.loc[i]['품사']])
                point.append(df1.loc[i]['가중치'])
                break
    service.all_new_weight(service.one_new_weight(rematch))
    count = len(point)
    result_point=0
    point.sort(reverse=True)
    if count ==1:
        high_point = point[0]
        mid_point= point[0]
        low_point =point[0]
    elif count==2:
        high_point =point[0]
        mid_point= sum[point]/2
        low_point= point[1]
    elif count == 3:
        high_point = point[0]
        mid_point = point[1]
        low_point = point[2]
    else:
        high_point = sum(point[:int(count*0.3)])/len(point[:int(count*0.3)])
        mid_point = sum(point[int(count*0.3):int(count*0.6)])/len(point[int(count*0.3):int(count*0.6)])
        low_point = sum(point[int(count*0.6):])/len(point[int(count*0.6):])
    if count>=5 and low_point>1.5 :
        result_point = 5+count/5
    elif (mid_point+low_point)/2>1.4 or (high_point+mid_point+low_point)/3>1.6 or high_point>1.94:
        result_point = 4+count/5
    elif (high_point+mid_point+low_point)/3>1.3:
        result_point = 3+ count/5
    elif (high_point+mid_point+low_point)/3>1.0:
        result_point =2 + count/5
    elif (high_point+mid_point+low_point)/3>0.5:
        result_point = 1+count/5
    else:
        result_point = count/5

    #Log Insert
    log = Log()
    log.score = result_point
    log.deviceId_id = deviceId
    log.save()

    return None