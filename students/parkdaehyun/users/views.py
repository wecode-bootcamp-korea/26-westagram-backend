import json
import re

from django.http import JsonResponse, request
from django.views import View
from django.shortcuts import render

from .models import User

# Create your views here.

class UserlistView(View):
    def post(self, request):
        data= json.loads(request.body)
        email_validation     = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        password_validation  = re.compile("^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$")

        if data["email"] == "" or data["password"] == "":
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            
        if not email_validation.match(data["email"]):
            return JsonResponse({"message" : "이메일 형식이 잘못됐습니다."}, status=400)

        if not password_validation.match(data["password"]):
            return JsonResponse({"message" : "비밀번호 형식이 잘못됐습니다."}, status=400)

        if User.objects.filter(email=data["email"]).exists():
            return JsonResponse({"message" : "동일한 이메일이 존재합니다."}, status=400)
        
        else:
            User.objects.create(
            name                 = data["name"],
            email                = data["email"],
            password             = data["password"],
            telephone            = data["telephone"],
            personal_information = data["personal_information"],
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        
        
