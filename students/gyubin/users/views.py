import json, re

from django.http     import JsonResponse
from django.views    import View

from users.models import User

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            name     = data['name']	
            email    = data['email']
            password = data['password']
            contact  = data['contact']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EMAIL_EXISTS"}, status=409)

            User.objects.create(
                name = name,
                email = email,
                password = password,
                contact = contact,
            )

            return JsonResponse({'MESSAGE' : 'CREATED'}, status=201)

        except KeyError:
            return  JsonResponse({"error_message" : "Key_Error"}, status = 400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email, password=password).exists():
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)

        except KeyError:
            return  JsonResponse({"error_message" : "Key_Error"}, status = 400)