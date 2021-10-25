import json, re, bcrypt, jwt

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM

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

            bcrypt_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            User.objects.create(
                name         = name,
                email        = email,
                password     = bcrypt_password.decode('utf-8'),
                phone_number = phone_number,
                age          = age
            )
            return HttpResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except:
            return HttpResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            email    = data['email']
            password = data['password']

            user     = User.objects.get(email = email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                jwt_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm = ALGORITHM)
                return HttpResponse({'ACCESS_TOKEN' : jwt_token},{'MESSAGE':'SUCCESS'}, status = 200)
            else:
                return HttpResponse({'MESSAGE':'WRONG_PASSWORD'}, status = 401)

        except KeyError:
            return HttpResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)
        except User.DoesNotExist:
            return HttpResponse({"MESSAGE":"NOT_EXISTED_USER"}, status = 401)