import json
import bcrypt
import jwt

from django.http    import JsonResponse
from django.views   import View

from .models    import User
from .utils     import validate_email, validate_password, validate_phone

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']

            user = User.objects.get(email=email, password=password)
            
            # user check
            if not user:
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            return JsonResponse({"message": "SUCCESS"}, status=200)
            
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            name         = data["name"]
            email        = data['email']
            password     = data['password']
            phone_number = data["phone_number"]
            url          = data["url"]

            if not validate_email(email):
                return JsonResponse({"message": "VALIDATION_ERROR : EMAIL OR PASSWORD"}, status=400)

            if not validate_password(password):
                return JsonResponse({"message": "VALIDATION_ERROR : EMAIL OR PASSWORD"}, status=400)

            if not validate_phone(phone_number):
                return JsonResponse({"message": "VALIDATION_ERROR : PHONE NUMBER"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "DUPLICATE_EMAIL_ERROR"}, status=409)

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
                url          = url,
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
