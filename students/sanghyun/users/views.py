import json, re, bcrypt, jwt

from django.http        import JsonResponse
from django.views       import View

from users.models       import User
from westagram.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:        
            data        = json.loads(request.body)
            name        = data['name']
            password    = data['password']
            birth       = data['birth']
            email       = data['email']
            mobile      = data['mobile']
            sns_address = data['sns_address']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EMAIL_EXISTS"}, status=409)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name        = name,
                password    = hashed_password,
                birth       = birth,
                email       = email,
                mobile      = mobile,
                sns_address = sns_address,
            )
            return JsonResponse({'MESSAGE':'CREATED'}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400) 

class LogInView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data['email']
            password    = data['password']
            user_info   = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode("utf-8"), user_info.password.encode("utf-8")):
                return JsonResponse({"MESSAGE": "CHECK_YOUR_EMAIL/PASSWORD"}, status = 400)
                
            token = jwt.encode({'id': user_info.id}, SECRET_KEY, algorithm = ALGORITHM)
            return JsonResponse({'MESSAGE' : 'LOGIN_SUCCESS', 'TOKEN' : token}, status = 200)

        except KeyError:
            return  JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"MESSAGE": "CHECK_YOUR_EMAIL/PASSWORD"}, status = 401) 