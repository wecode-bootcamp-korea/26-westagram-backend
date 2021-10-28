import json, re
import bcrypt
import jwt

from django.conf import settings
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
        try:
            data        = json.loads(request.body)
            user        = User.objects.get(email=data["email"])
            access_token= jwt.encode({'id' : user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

            if User.objects.filter(email=data["email"]).exists():
                if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
                    return JsonResponse({"message" : "INVALID_USER"}, status=401)
                return JsonResponse({"token" : access_token}, status=200) 

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)