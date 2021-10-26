import json, re, bcrypt, jwt

from django.http     import JsonResponse
from django.views    import View

from users.models import User
from westagram.settings import SECRET_KEY

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

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password.decode('utf-8'),
                contact  = contact,
            )

            return JsonResponse({'message' : 'CREATED'}, status=201)

        except KeyError:
            return  JsonResponse({"error_message" : "Key_Error"}, status = 400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email    = User.objects.get(email=data['email'])
            password = data['password']

            if bcrypt.checkpw(password.encode('utf-8'), email.password.encode('utf-8')):
                token = jwt.encode({'id': email.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'message' : 'SUCCESS', 'token' : token}, status=200)

            return JsonResponse({"message": "INVALID_USER"}, status = 401)

        except KeyError:
            return  JsonResponse({"error_message" : "Key_Error"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"error_message":"NOT_EXISTED_USER"}, status = 401) 