from konlpy.tag import Kkma
from konlpy.utils import pprint
import json
import pickle


def find_highligt(ko_sentiment):
    highlight_list=[]
    sentences = ko_sentiment['sentences']
    for stc in sentences:
        if stc['sentiment'] !='negative':
            continue
        else:
            highlight_list.append(stc['content'][int(stc['highlights'][0]['offset']):
                                                 int(stc['highlights'][0]['offset'])+int(stc['highlights'][0]['length'])])
    return highlight_list
def ko_sentences_bytxt():
    temp_list=[]
    fopen=open(r'C:\Users\user\Desktop\testdata.txt','r')
    temp=fopen.readline()
    temp=temp.replace('\x00','')
    start=0
    end=temp.find('document', 3)-2
    while True:
        try:
            tempdict=json.loads(temp[start:end])
            start=end
            end = temp.find('document', start+3)-2
            temp_list+=find_highligt(tempdict)
        except:
            tempdict=json.loads(temp[start:])
            temp_list+=find_highligt(tempdict)
            break
    with open(r"C:\Users\user\Desktop\data.pickle", "wb") as fw:
        pickle.dump(temp_list, fw)