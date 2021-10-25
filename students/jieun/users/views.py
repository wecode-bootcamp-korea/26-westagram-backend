import json, bcrypt, jwt

from django.http    import JsonResponse
from django.views   import View

from users.models   import User
from users.utils    import validate_email, validate_password, validate_phone
from my_settings    import JWT

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)
            
            is_valid_password = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
            if not is_valid_password:
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            token = jwt.encode(
                {
                    'user_id': user.id, 
                    'exp'    : JWT['EXP_IN_SEC']
                }
                , JWT['SECRET']
                , algorithm = JWT['ALGORITHM']
            )
            return JsonResponse({"message": "SUCCESS", "token" : token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)


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

            salt      = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_pw,
                phone_number = phone_number,
                url          = url,
            )
            return JsonResponse({"message": "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
