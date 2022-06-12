from django.shortcuts import render
from .models import User, Device
from naverapi.models import Log
import json
import bcrypt
import jwt
from django.http import HttpResponse, JsonResponse
from server.my_settings import SECRET_KEY, ALGORITHM
from django.db.models import F, Func, Value, CharField
import base64

# Create your views here.

# Register
def register(request):
    if request.method == 'POST':
        try:
            # 회원가입 loading DATA: 아이디, 패스워드, 사용자 이름, 사용자 나이
            # JSON DATA LOADING
            input = request.body.decode('utf-8').split("&")
            userId = ""
            userPassword = ""
            userName = ""
            deviceId = ""
            for i in input:
                temp = i.split("=")
                if temp[0] == "userId":
                    userId = temp[1]
                elif temp[0] == "userPass":
                    userPassword = temp[1]
                elif temp[0] == "userName":
                    userName = temp[1]
                elif temp[0] == "deviceId":
                    deviceId = temp[1]
                else:
                    continue

            #Bcrypt Password encryption
            #Making Salt
            new_salt = bcrypt.gensalt()
            #인코딩을 하여 "PW"의 bytes 변환
            new_password = userPassword.encode('utf-8')
            hashed_password = bcrypt.hashpw(new_password, new_salt)

            #비밀번호 문자열 변환
            hash_pw = hashed_password.decode('utf-8')

            #사용자 정보
            user = User()
            user.Id = userId
            user.Pw = hash_pw
            user.userName = userName

            #사용자 정보 저장
            result = user.save()

            #사용자 ID 호출
            userId = User.objects.latest('userId')

            #디바이스 등록
            device = Device()
            device.deviceId = deviceId
            device.userId = userId
            device.save()

            # 처리결과 전송
            data = {
                "success": True
            }
            return JsonResponse(data)

        except Exception as e:
            data = {
                "success": False
            }
            return JsonResponse(data)

#login
def login(request):
    if request.method == "POST":
        try:
            #JSON LOAD
            input = request.body.decode('utf-8').split("&")
            for i in input:
                temp = i.split("=")
                if temp[0] == "userId":
                    userId = temp[1]
                elif temp[0] == "userPass":
                    userPassword = temp[1]
                else:
                    continue
            targetUser = User.objects.get(Id=userId)
            bytes_inputPw = userPassword.encode('utf-8')
            bytes_userPw = targetUser.Pw.encode('utf-8')
            if bcrypt.checkpw(bytes_inputPw, bytes_userPw):
                data = {'userId': targetUser.userId}
                token = jwt.encode(data, SECRET_KEY, ALGORITHM).decode('utf-8')
                print(token)
                data = {
                    "success": True,
                    "token": token
                }
                return JsonResponse(data)
        except Exception as e:
            print(e)
            data = {
                "success": False
            }
            return JsonResponse(data)

#Give Data
def giveData(request):
    if request.method == "POST":
        try:
            #JSON LOADS
            input = request.body.decode('utf-8').split("&")
            for i in input:
                temp = i.split("=")
                if temp[0] == "token":
                    token = temp[1]
                else:
                    continue
            targetId = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["userId"]
            devices = Device.objects.filter(userId = targetId)
            data = Log.objects.filter(deviceId_id__in=devices.values('deviceId')).values()
            data = data.annotate(
                logDate = Func(
                    F('logDate'),
                    Value('%m.%d %H'),
                    function='DATE_FORMAT',
                    output_field=CharField()
                )
            )
            data = list(data)
            newObj = {
                "success": True,
                "logList": data
            }
            return JsonResponse(newObj)
        except Exception as e:
            print(e)
            data = {
                "success": False
            }
            return JsonResponse(data)