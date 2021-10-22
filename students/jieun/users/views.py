import json

from django.http    import JsonResponse
from django.views   import View

from .models    import User
from .utils     import validate_email, validate_password, validate_phone

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

            found = User.objects.filter(email=email).exists()
            if found:
                return JsonResponse({"message": "DUPLICATE_EMAIL_ERROR"}, status=400)

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
