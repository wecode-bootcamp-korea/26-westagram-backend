import json
import re
import bcrypt
import jwt

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
            hashed_password = bcrypt.hashpw( password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if not re.match('^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) :
                return JsonResponse({"message": "E-mail is not valued"}, status = 400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password) :
                return JsonResponse({"message": "Password error"}, status = 400)
            
            if User.objects.filter(email = email).exists() :
                return JsonResponse({"message": "Duplicated email"}, status = 400)
            
            User.objects.create(
                name          = name,
                email         = email,
                password      = hashed_password,
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
            email           = data["email"] 
            password        = data["password"]
            hashed_Password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user            = User.objects.get(email=email)
            encoded_jwt     = jwt.encode({'user-id' : user.id}, 'secret', algorithm = 'HS256')

            if not User.objects.filter(email=email).exists() :
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            if bcrypt.checkpw(password.encode('utf-8'), hashed_Password.encode('utf-8')):
                return JsonResponse({"message": "SUCCESS", "jwt": encoded_jwt}, status = 200)

        except KeyError : 
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)