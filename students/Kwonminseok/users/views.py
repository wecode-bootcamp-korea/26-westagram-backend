import json
import re

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from .models import User

class SignUpView(View):
    def post(self, request):       
        try:
            data           = json.loads(request.body)
            name           = data["name"]
            email          = data["email"]
            password       = data["password"]
            phone_number   = data["phone_number"]
            age            = data["age"]
 
            if not (password and email):
                return JsonResponse({'message' : 'NO_VALUE'}, status=400)
            if not re.match('^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message' : 'EMAIL_VALIDATION_ERROR'}, status=400)
            if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({'message' : 'PASSWORD_VALIDATION_ERROR'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'DUPLICATED EMAIL'}, status=400)
            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
                age          = age
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)         
       
             
