from django.shortcuts import render
from .models import User, Device
import json
import bcrypt
import jwt
from django.http import HttpResponse, JsonResponse
from server.my_settings import SECRET_KEY, ALGORITHM

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

            return HttpResponse(result)

        except Exception as e:
            return "Error Emerged: " + e

#login
def login(request):
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
            return HttpResponse(jwt.encode(data, SECRET_KEY, ALGORITHM).decode('utf-8'))
    except Exception as e:
        return "Error Emerged: " + e
