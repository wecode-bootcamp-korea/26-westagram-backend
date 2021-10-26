import json
from os import name
import re
import bcrypt

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import User

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
            name        = data.get("name"), 
            email       = data.get("email"),
            password    = (bcrypt.hashpw(data.get("password").encode('utf-8'), bcrypt.gensalt())).decode('utf-8'),
            phone_num   = data.get("phone_num"),
            )
        
        return JsonResponse({"message" : "SUCCESS"}, status=201)

class LoginView(View):
    def post(self, request):
        data        = json.loads(request.body)
        email       = data.get("email")
        password    = data.get("password")

        if not (email or password):
            return JsonResponse({"messgae" : "KEY_ERROR"}, status=400)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if bcrypt.checkpw(data.get("password").encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "SUCCESS"}, status=200)

        return JsonResponse({"message" : "INVALID_USER"}, status=401)
