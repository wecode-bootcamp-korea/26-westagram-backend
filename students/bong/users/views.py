import json
import re
import bcrypt, jwt

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .models import User


class SignupView(View):
    def post(self, request):
        data        = json.loads(request.body)
        name        = data["name"]
        email       = data["email"]
        password    = data["password"]
        phone_num   = data["phone_num"]

        if not (email and password):
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
        if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return JsonResponse({"message" : "EMAIL_VALIDATION_ERROR"}, status=400)

        if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,}$', password):
            return JsonResponse({"message" : "PASSWORD_VALIDATION_ERROR"}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=400)

        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        User.objects.create(
            email       = email, 
            password    = hashed_password,
            name        = name,
            phone_num   = phone_num
            )
        
        return JsonResponse({"message" : "SUCCESS"}, status=201)

class LoginView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            email           = data["email"]
            password        = data["password"]
            user = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return JsonResponse({"MESSAGE" : "SUCCESS", "ACCESS_TOKEN" : access_token}, status=200)
                
        except User.DoesNotExist:
            return JsonResponse({"message" : "USER_DOES_EXISTS"}, status=401) 

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)               