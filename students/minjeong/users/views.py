import json, re

from django.http    import JsonResponse
from django.views   import View

from .models   import User

class UserView(View):
    def post(self, request):        

        try:
            data = json.loads(request.body)
            name          = data['name']
            email         = data['email']
            password      = data['password']
            phone_number  = data['phone_number']
            personal_info = data['personal_info']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message':'EMAIL_NOT_VALID'}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({'message':'PASSWORD_NOT_VALID'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'SAME_EMAIL_ERROR'}, status = 400)

            User.objects.create(
                name          = name,
                email         = email,
                password      = password,
                phone_number  = phone_number,
                personal_info = personal_info
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class LoginView(View):
    def post(slef, request):

        try:
            data = json.loads(request.body)
            email         = data['email']
            password      = data['password']

            # 계정을 잘못 입력한 경우 -> {'message' : 'INVALID_USER'}, status code 401
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            # 비밀번호를 잘못 입력한 경우 -> {'message' : 'INVALID_USER'}, status code 401
            if not User.objects.filter(password=password).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
            
            User.objects.get(
                email    = email,
                password = password
            )

            # 로그인 성공
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            # 계정이나 패스워드 키가 전달되지 않았을 경우 -> {'message' : 'KEY_ERROR'}, status code 400
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
