import json
import re
import bcrypt, jwt

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import User
from my_settings import SECRET_KEY

class SignupView(View):
    def post(self, request):
        data        = json.loads(request.body)
        name        = data.get("name")
        email       = data.get("email")
        password    = data.get("password")
        phone_num   = data.get("phone_num")

        if not (email and password):
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
        if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return JsonResponse({"message" : "EMAIL_VALIDATION_ERROR"}, status=400)

        if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,}$', password):
            return JsonResponse({"message" : "PASSWORD_VALIDATION_ERROR"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=400)

        User.objects.create(
            name, email, phone_num,
            password    = (bcrypt.hashpw(data.get("password").encode('utf-8'), bcrypt.gensalt())).decode('utf-8'),
            )
        
        return JsonResponse({"message" : "SUCCESS"}, status=200)

class LoginView(View):
    def post(self, request):
        data            = json.loads(request.body)
        email           = data.get("email")
        password        = data.get("password")
        
        if not (email and password):
            return JsonResponse({"messgae" : "KEY_ERROR"}, status=400)
       
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({"email" : email}, SECRET_KEY, algorithm='HS256')
                return JsonResponse({"TOKEN" : token}, status=200)
                
        return JsonResponse({"message" : "INVALID_USER"}, status=401)            