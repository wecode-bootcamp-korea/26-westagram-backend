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
            
            if not data['email'] or not data['password']:
                return HttpResponse({'MESSAGE' : 'NO_INPUT_DATA'}, status=400)

            email_validation = re.compile(
                "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$"
                )
            password_validation = re.compile(
                "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
                )

            if (email_validation.match(data['email'])) is None:
                return HttpResponse({"MESSAGE" : "INVALID_EMAIL"}, status=403)

            if (password_validation.match(data['password'])) is None:
                return HttpResponse({"MESSAGE" : "INVALID_PASSWORD"}, status=403)

            if User.objects.filter(email=data['email']).exists():
                return HttpResponse({"MESSAGE" : "ALREADY EXISTED"}, status=409)

            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone_number'],
                age          = data['age']
            )
            return HttpResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except:
            return HttpResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)