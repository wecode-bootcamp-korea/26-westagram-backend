import json, bcrypt, jwt

from django.http    import JsonResponse
from django.views   import View

from django.conf import settings

from .models        import User
from .utils         import validate_email, vaildate_password

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        try : 
            name     = data['name']
            email    = data['email']
            password = data['password']
            number   = data['number']
            nickname = data['nickname']

            if not validate_email(email) :
                return JsonResponse({'MASSAGE':'VALIDATION_ERROR'}, status=400)

            if not vaildate_password(password) :
                return JsonResponse({'MASSAGE':'PW_VALIDATION_ERROR'}, status=400)
        
            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS_EMAIL'}, status=409)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
               name     = name,
               email    = email,
               password = hashed_password,
               number   = number,
               nickname = nickname,
            )             
            return JsonResponse({'MASSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try :
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'UserID': user.id}, settings.SECRET_KEY,algorithm=settings.ALGORITHM ).decode('utf-8')
                return JsonResponse({'ACCESS_TOKEN': access_token}, status=200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except User.DoesNotExist :
            return JsonResponse({'MASSAGE':'USER_DOES_NOT_EXISTS'}, status = 401) 
            