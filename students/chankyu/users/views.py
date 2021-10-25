import json, re

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views import View

from users.models import User

# Create your views here.
class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            age          = data['age']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return HttpResponse({"MESSAGE" : "INVALID_EMAIL"}, status=403)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return HttpResponse({"MESSAGE" : "INVALID_PASSWORD"}, status=403)

            if User.objects.filter(email=email).exists():
                return HttpResponse({"MESSAGE" : "ALREADY EXISTED"}, status=409)

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
                age          = age
            )
            return HttpResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except:
            return HttpResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            if email == "" or password =="":
                return HttpResponse({"MESSAGE" : "NO_INPUT_DATA"}, status = 400)
            
            if not User.objects.filter(email = email).exists():
                return HttpResponse({"MESSAGE" : "INVALID_EMAIL"}, status = 401)
            
            if password != User.objects.get(email = email).password:
                return HttpResponse({"MESSAGE" : "INVALID_PASSWORD"}, status = 401)

            return HttpResponse({"MESSAGE": "SUCCESS"}, status = 200)

        except:
            return HttpResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)