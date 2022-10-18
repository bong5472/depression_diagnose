import requests, json
from django.conf import settings
from datetime import datetime
import pickle
from .modules import service
import pandas as pd
import os
from celery import shared_task
from .models import Log
from django.core.files.storage import default_storage
from .depression_judgement import Depression_judgment
from django.db import connection


@shared_task
def sentiment_analysis(temp, deviceId):
    print(temp)
    currentPath = os.getcwd()
    if 'negative' not in temp[0].split(":")[2]:
        return 0
    pathname = os.path.join(currentPath, "naverapi", "modules", "asset", "clova_data_dump.pickle")
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
    print(point)
    if count == 1:
        if point[0] > 1:
            high_point = point[0] - 0.5
            mid_point = high_point / 2
            low_point = mid_point / 2
        else:
            high_point = point[0]
            mid_point = point[0] / 2
            low_point = point[0] / 3
    elif count == 2:
        if point[0] > 1.5:
            high_point = point[0] - 0.3
            mid_point = (point[0] + point[1]) / 2 - 0.3
            low_point = point[1] - 0.3
        else:
            high_point = point[0]
            mid_point = (point[0] + point[1]) / 2
            low_point = point[1]
    elif count == 3:
        high_point = point[0]
        mid_point = point[1]
        low_point = point[2]
    else:
        high_point = sum(point[:int(count*0.3)])/len(point[:int(count*0.3)])
        mid_point = sum(point[int(count*0.3):int(count*0.6)])/len(point[int(count*0.3):int(count*0.6)])
        low_point = sum(point[int(count*0.6):])/len(point[int(count*0.6):])
    if count>10:
        count=10
    if count>=5 and low_point>1.6 :
        result_point = 5+count/7
    elif (mid_point+low_point)/2>1.6 or (high_point+mid_point+low_point)/3>1.7 or (high_point>1.94 and count>=5):
        result_point = 4+count/7
    elif (high_point+mid_point+low_point)/3>1.5:
        result_point = 3+ count/7
    elif (high_point+mid_point+low_point)/3>1.0:
        result_point =2 + count/7
    elif (high_point+mid_point+low_point)/3>0.5:
        result_point = 1+count/7
    else:
        result_point = count/7
    print(result_point)

    #Log Insert
    log = Log()
    log.score = result_point
    log.deviceId_id = deviceId
    log.save()

    return None


@shared_task
def depression_messaging(deviceId):
    # SQL을 이용하여 DataBase에서 우울 로그 추출
    try:
        # SQL LOADING
        cur = connection.cursor()
        sql = "SELECT score FROM log WHERE deviceId = %s ORDER BY logDate DESC LIMIT 3"
        result = cur.execute(sql, [deviceId])
        data = cur.fetchall()
        connection.close()
        argument = []

        # Data Converting
        for i in data:
            argument.append(i[0])

        # 이를 기반으로 함수에서 처리
        decision_result = Depression_judgment(argument)
        print(decision_result)

        # 결과값 판정하여 메세지 보낼지 말지 여부 결정
        # Firebase Cloud Messaing(FCM) 이용 ==> 추후 추가 연동
        if decision_result == 3:
            # 심각한 우울증
            print("hard")
        elif decision_result == 2:
            # 우울감
            print("sad")
        else:
            # 우울증 아님
            print("normal")

    except Exception as e:
        print("Error Emerged")
        print(e)
        connection.rollback()
        connection.close()