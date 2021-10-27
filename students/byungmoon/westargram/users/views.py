import json, re, bcrypt

from django.http      import JsonResponse
from django.views     import View

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

            User.objects.create(
                name               = name,
                email              = email,
                password           = (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8'),
                contact            = contact,
                other_personal_inf = other_personal_inf
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
                return JsonResponse({"error_message" : "KEY_ERROR"}, status = 400)

class SignInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email, password=password).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            return JsonResponse({"message": "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"error_message": "KEY_ERROR"}, status=400)