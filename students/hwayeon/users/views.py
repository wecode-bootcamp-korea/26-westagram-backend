import json, re, bcrypt

from django.http import JsonResponse
from django.views import View

from .models import User

class SignupView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            username     = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone']

            if not re.match('^[\w+-]+@[\w]+\.[\w.]+$', email):
                return JsonResponse({"message": "Email format is not valid"}, status=400)

            if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*-+_=?]).{8,}$', password):
                return JsonResponse({"message": "Password_Validation_Error"}, status=400)

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message": "Email_Exist_Error"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                username     = username,
                email        = email,
                password     = hashed_password.decode('utf-8'),
                phone_number = phone_number
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "Key_Error"}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']

            if not User.objects.filter(email = email, password = password).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "Key_Error"}, status=400)