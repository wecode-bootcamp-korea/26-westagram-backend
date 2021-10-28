import json, re, bcrypt, jwt

from django.http      import JsonResponse
from django.views     import View
from django.conf.settings import ALGORITHM, SECRET_KEY

from .models     import User

class SignUpView(View):
    def post(self, request):
        try:
            data               = json.loads(request.body)
            name               = data['name']
            email              = data['email']
            password           = data['password']
            contact            = data['contact']
            other_personal_inf = data['other_personal_inf']
            
            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EMAIL_EXISTS"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                name               = name,
                email              = email,
                password           = hashed_password,
                contact            = contact,
                other_personal_inf = other_personal_inf
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
                return JsonResponse({"error_message" : "KEY_ERROR"}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)

            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data["password"].encode("utf-8"), hashed_password):
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)

            access_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({"MESSAGE":"SUCCESS", "ACCESS_TOKEN": access_token}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)