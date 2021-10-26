import json
import re

from django.http import JsonResponse
from django.views import View

from .models import User

class UserListView(View):
    def post(self, request) : 
        
        data = json.loads(request.body)

        try : 
            name          = data["name"]
            email         = data["email"] 
            password      = data["password"]
            contact       = data["contact"]
            date_of_birth = data["date_of_birth"]
            hobby         = data["hobby"]
            
            if not re.match('^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) :
                return JsonResponse({"message": "E-mail is not valued"}, status = 400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password) :
                return JsonResponse({"message": "Password error"}, status = 400)
            
            if User.objects.filter(email = email).exists() :
                return JsonResponse({"message": "Duplicated email"}, status = 400)
            
            User.objects.create(
                name          = name,
                email         = email,
                password      = password,
                contact       = contact,
                date_of_birth = date_of_birth,
                hobby         = hobby
            )

            return JsonResponse({"message": "SUCCESS"}, status = 201)
        
        except KeyError : 
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

class LogInView(View) : 
    def post(self, request):

        data = json.loads(request.body)

        try : 
            email         = data["email"] 
            password      = data["password"]
            
            if not (email or password): 
                return JsonResponse({"message": "KEY_ERROR"}, status = 400)

            if not User.objects.filter(email=email).exists() :
                return JsonResponse({"message": "INVALID_USER"}, status = 401)
            
            if not User.objects.filter(password=password).exists() :
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            return JsonResponse({"message": "SUCCESS"}, status = 201)

        except KeyError : 
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)