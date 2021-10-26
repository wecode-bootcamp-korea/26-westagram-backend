import json
from os import name
import re

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
            name        = data["name"], 
            email       = data["email"],
            password    = data["password"],
            phone_num   = data["phone_num"],
            )
        
        return JsonResponse({"message" : "SUCCESS"}, status=201)

class LoginView(View):
    def post(self, request):
        data        = json.loads(request.body)
        email       = data.get("email")
        password    = data.get("password")

        if not (email or password):
            return JsonResponse({"messgae" : "KEY_ERROR"}, status=400)

        if not User.objects.filter(email=email, password=password):
            return JsonResponse({"message" : "INVALID_USER"}, status=401)

        return JsonResponse({"message" : "SUCCESS"}, status=200)


