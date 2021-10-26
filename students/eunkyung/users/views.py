import json

from django.http    import JsonResponse
from django.views   import View

from .models        import User
from .utils         import validate_email, vaildate_password

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
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

            User.objects.create(
               name     = name,
               email    = email,
               password = password,
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

            if not User.objects.filter(email=email, password=password).exists():
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)
                
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)