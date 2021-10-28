import json, re
import bcrypt

from django.http import JsonResponse, request
from django.views import View

from .models import User

class UserlistView(View):
    def post(self, request):
        data            = json.loads(request.body)
        REGEX_EMAIL     = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGEX_PASSWORD  = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

        if not (data.get("password") and data.get("email")):
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            
        if not re.match(REGEX_EMAIL, data["email"]):
            return JsonResponse({"message" : "이메일 형식이 잘못됐습니다."}, status=400)

        if not re.match(REGEX_PASSWORD, data["password"]):
            return JsonResponse({"message" : "비밀번호 형식이 잘못됐습니다."}, status=400)

        if User.objects.filter(email=data["email"]).exists():
            return JsonResponse({"message" : "동일한 이메일이 존재합니다."}, status=400)

        hashed_password = (bcrypt.hashpw(data["password"].encode("utf-8")), bcrypt.genslat()).decode("utf-8")
        
        User.objects.create(
            name                 = data["name"],
            email                = data["email"],
            password             = hashed_password,
            telephone            = data["telephone"],
            personal_information = data["personal_information"],
        )

        return JsonResponse({"message" : "SUCCESS"}, status = 201)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not (data.get("password") and data.get("email")):
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        if not User.objects.filter(email=data["email"], password=data["password"]).exists():
            return JsonResponse({"message" : "INVALID_USER"}, status=401) 

        return JsonResponse({"message" : "SUCCESS"}, status = 200)