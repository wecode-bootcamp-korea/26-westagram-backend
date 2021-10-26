import json, re, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from my_settings            import SECRET_KEY, ALGORITHM

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

            if not re.match('^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message' : 'EMAIL_VALIDATION_ERROR'}, status=400)

            if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password):
                return JsonResponse({'message' : 'PASSWORD_VALIDATION_ERROR'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'DUPLICATED EMAIL'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password,
                phone_number = phone_number,
                age          = age
            )

            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data["email"]
            password     = data["password"]

            if not User.objects.filter(email=email):
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)

            if bcrypt.checkpw(password.encode('utf-8'), User.password.encode('utf-8')):
                token = jwt.eoncode({'email' : email}, SECRET_KEY, algorithm = ALGORITHM)
                token = token.decode('utf-8')
                return JsonResponse({'token' : token}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
