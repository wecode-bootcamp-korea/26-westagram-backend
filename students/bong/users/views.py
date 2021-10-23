import json
from os import name
import re

from django.views import View
from django.http import HttpResponse, JsonResponse

from .models import User

class UserView(View):
    def post(self, request):
        data                = json.loads(request.body)
        name                = data["name"]
        email               = data["email"]
        password            = data["password"]
        phone_num           = data["phone_num"]
        email_validation    = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password_validation = re.compile(r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~₩!@#$%^&*()\-_=+])[a-zA-Z0-9~!@#$%^&*()_\-+=]{8,}$')

        if email == "" or password == "":
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
    
        if not email_validation.match(email):
            return JsonResponse({"message" : "EMAIL_VALIDATION_ERROR"}, status=400)

        if not password_validation.match(password):
            return JsonResponse({"message" : "PASSWORD_VALIDATION_ERROR"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"message" : "DUPLICATION_ERROR"}, status=400)

        User.objects.create(
            name=data["name"], 
            email=data["email"],
            password=data["password"],
            phone_num=data["phone_num"],
            #created_at=data["created_at"],
            #updated_at=data["updated_at"],
            )
        
        return JsonResponse({"message" : "SUCCESS"}, status=201)
