import json
import re

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from .models import User

class SignUpView(View):
    def post(self, request):
        data           = json.loads(request.body)
        regex_email    = re.compile('^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        regex_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
       
        try:
            if data["email"] == "" or data["password"] == "":
                return JsonResponse({'message' : 'NO_VALUE'}, status=400)
            if not regex_email.match(data["email"]):
                return JsonResponse({'message' : 'EMAIL_VALIDATION_ERROR'}, status=400)
            if not regex_password.match(data["password"]):
                return JsonResponse({'message' : 'PASSWORD_VALIDATION_ERROR'}, status=400)
            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({'message' : 'DUPLICATED EMAIL'}, status=400)
            User.objects.create(
                name         = data["name"],
                email        = data["email"],
                password     = data["password"],
                phone_number = data["phone_number"],
                age          = data["age"]
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)         
       
             
