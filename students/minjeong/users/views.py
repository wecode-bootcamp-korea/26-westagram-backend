import json, re, bcrypt, jwt

from django.http    import JsonResponse
from django.views   import View

from .models     import User
from django.conf import settings

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

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name          = name,
                email         = email,
                password      = hashed_password,
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
            user          = User.objects.get(email=email)
            access_token  = jwt.encode({'user_id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

            return JsonResponse({'message' : 'SUCCESS', 'ACCESS_TOKEN' : access_token}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist :
            return JsonResponse({"message" : "Unauthorized"}, status = 401) 

