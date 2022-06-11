from django.shortcuts import render
from django.http import HttpResponse
import time
import requests, json
from django.conf import settings
from konlpy.tag import Komoran
import pandas as pd
from konlpy.utils import pprint
import json
import pickle
import openpyxl
from openpyxl import load_workbook
import os
# 엑셀 데이터셋 -> 문자열 추출 함수
# AI 허브 데이터 셋 기준 문자열 추출 함수
# 파일 경로 및 엑셀 서식에 맞춰 코드 수정 필요
currentPath = os.getcwd()
def excel_to_txt():
    templist = []
    temp = ''
    load_ex = load_workbook(r' 엑셀현재 path')
    f = open(r'.\naverapi\modules\asset\excel_to_data.txt ', 'a')
    load_ex = load_ex['Sheet1']
    get_cell0 = load_ex['F2':'F9357']
    get_cell1 = load_ex['H2':'H9375']
    get_cell2 = load_ex['J2':'J9375']
    get_cell3 = load_ex['L2':'L9375']
    get_cell4 = load_ex['N2':'N5131']
    for row0, row1, row2, row3, row4 in zip(get_cell0, get_cell1, get_cell2, get_cell3, get_cell4):
        for cell0, cell1, cell2, cell3, cell4 in zip(row0, row1, row2, row3, row4):
            if cell0.value == '기쁨':
                break
            temp += cell1.value
            if len(temp) > 900:
                templist.append(temp)
                temp = ''
            if type(cell2.value) == type(' '):
                temp += cell2.value
            if len(temp) > 900:
                templist.append(temp)
                temp = ''
            if type(cell3.value) == type(' '):
                temp += cell3.value
            if len(temp) > 900:
                templist.append(temp)
                temp = ''
            if type(cell4.value) == type(' '):
                temp += cell4.value
            if len(temp) > 900:
                templist.append(temp)
                temp = ''
    for i in templist:
        temp = i.replace(u'\xa0', u' ')
        f.write(temp)
        f.write('\n')

# clova 과부하 대비 분할 데이터 병합 데이터(필요시 사용, 현재 사용 X)
def pickle_merge():
    data=[]
    for i in range(1,24):
        with open(r'.\naverapi\modules\asset\final_data.pickle','rb') as fr:
            data.append(pickle.load(fr))
        with open(r'.\naverapi\modules\asset\clova_data_dump.pickle','rb') as fr:
            data.append(pickle.load(fr))
    with open(r'.\naverapi\modules\final_data.pickle','wb') as fw:
        pickle.dump(data,fw)

# clova 데이터 하이라이트 문자열 추출
# 파라미터는 clova return 딕셔너리
def find_highligt(ko_sentiment):
    highlight_list=[]
    if 'status' in ko_sentiment.keys():
        return []
    sentences = ko_sentiment['sentences']
    for stc in sentences:
        if stc['sentiment'] !='negative':
            continue
        else:
            highlight_list.append(stc['content'][int(stc['highlights'][0]['offset']):
                                                 int(stc['highlights'][0]['offset'])+int(stc['highlights'][0]['length'])])
    return highlight_list

#nlp 분석
def konlp(input):
    mean_list=['NNG','NNP','VV','VA','VCN','MM','MAG','IC']
    nlp_dict={}
    komoran=Komoran()
    text = input
    for i in text:
        temp=komoran.pos(i)
        for j in temp:
            if j[1]  not in mean_list:
                continue
            else:
                if j[0] in nlp_dict.keys():
                    nlp_dict[j[0]][1] += 1
                else:
                    nlp_dict[j[0]]=[j[1],1]

    return nlp_dict

#데이터 프레임 생성 함수
def frame_dict(x):
    frame = pd.DataFrame(x)
    df = frame.transpose()
    df.columns = ['품사','갯수']
    df=df.sort_values(by=['갯수'],ascending=[False])
    df.to_excel(excel_writer='nlpsort.xlsx')
    return df

#pickle 로드, 하이라이트 추출, nlp 분석함수,
#데이터 프레임 변환 및 저장을 동시에 진행하는 메인함수
def pickle_find_highlight():
    highligt=[]

    with open(currentPath + r'\naverapi\modules\asset\clova_data_dump.pickle', 'rb') as fr:
        data=pickle.load(fr)
        data=eval(data[0])
        highligt+=find_highligt(data)
    temp=konlp(highligt)
    frame_dict(temp).to_pickle(currentPath+r'\naverapi\modules\asset\final_data.pickle')

#가중치 갱신 함수
#1개 재계산
def one_new_weight(nlp_result):
    df = pd.read_pickle(currentPath + r'\naverapi\modules\asset\score_data.pickle')
    for k in range(len(nlp_result)):
        for i in range(len(df)):
            if nlp_result[k][0] in df.index[i] and nlp_result[k][1] == df['품사'][i]:
                df.iloc[i,1]+=1
                break
            elif i==len(df)-1:
                df2=pd.DataFrame({'품사':nlp_result[k][1],'갯수':1}, index=[nlp_result[k][0]])
                df = pd.concat([df,df2])
                df = df.sort_values(by=['갯수'], ascending=[False])
    return df
#전체 재계산
def all_new_weight(df):
    df['가중치']=0.0
    flag=df['갯수']>=5
    tmp_df=df[flag].drop_duplicates(['갯수'])
    score=round(1.95/len(tmp_df),8)
    df.iloc[0,2]=1.95
    k=1
    for i in range(1,len(df[flag])):
        if k>514:
            print('오류')
        if df['갯수'][i-1] == df['갯수'][i]:
            df.iloc[i,2]=1.95-(score*k)
        else:
            df.iloc[i,2] = 1.95 - (score * k)
            k+=1
    df.to_pickle(currentPath+r'\naverapi\modules\asset\score_data.pickle')