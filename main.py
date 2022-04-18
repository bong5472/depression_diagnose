import pandas as pd
import numpy as np
from konlpy.tag import Okt
tok=Okt()
dict_=dict()



##time sleep


with open('nlpinput.txt') as file:
    for line in file.readlines():
        system = tok.pos(line)
        for i in range(len(system)):
            if not system[i][0] in dict_:
                if(system[i][1]=='Noun'):
                    dict_[system[i][0]] = ['명사', 1]
                elif (system[i][1] == 'Verb'):
                    dict_[system[i][0]] = ['동사', 1]
                elif (system[i][1] == 'VerbPrefix'):
                    dict_[system[i][0]] = ['동사 접두사', 1]
                elif (system[i][1] == 'Josa'):
                    dict_[system[i][0]] = ['조사', 1]
                elif (system[i][1] == 'Adjective'):
                    dict_[system[i][0]] = ['형용사', 1]
                elif (system[i][1] == 'Suffix'):
                    dict_[system[i][0]] = ['접미사', 1]
                elif (system[i][1] == 'Adverb'):
                    dict_[system[i][0]] = ['부사', 1]
                elif (system[i][1] == 'Alpha'):
                    dict_[system[i][0]] = ['알파벳', 1]
                elif (system[i][1] == 'Conjunction'):
                    dict_[system[i][0]] = ['접속사', 1]
                elif (system[i][1] == 'Determiner'):
                    dict_[system[i][0]] = ['관형사', 1]
                elif (system[i][1] == 'Exclamation'):
                    dict_[system[i][0]] = ['감탄사', 1]
                elif (system[i][1] == 'Foreign'):
                    dict_[system[i][0]] = ['외국어, 한자 및 기타기호', 1]
                elif (system[i][1] == 'KoreanParticle'):
                    dict_[system[i][0]] = ['(ex: ㅋㅋ)', 1]
                elif (system[i][1] == 'Number'):
                    dict_[system[i][0]] = ['숫자', 1]
                elif (system[i][1] == 'PreEomi'):
                    dict_[system[i][0]] = ['선어말어미', 1]
                elif (system[i][1] == 'Punctuation'):
                    dict_[system[i][0]] = ['구두점', 1]
                elif (system[i][1] == 'Unknown'):
                    dict_[system[i][0]] = ['미등록어', 1]

        if (system[i][0]) in dict_:
            dict_[system[i][0]][1] += 1


print(dict_)
with open('nlpsort.txt','w',encoding='UTF-8') as f:
    for data, (name, num) in dict_.items():
        f.write(f'{data} : [{name},{num}]\n')

f.close()
file.close()

