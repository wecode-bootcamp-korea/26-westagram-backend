import json
import bcrypt
from django.http import JsonResponse
from django.views import View
from .models import Account
from .validate import validate_email, validate_password

# Create your views here.
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            username = data["username"]
            email = data["email"]
            password = data["password"]
            re_password = data["re_password"]
            phone_number = data["phone_number"]
            date_of_birth = data["date_of_birth"]

            if not validate_email(email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if not validate_password(password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if password != re_password:
                return JsonResponse({"message": "PASSWORD_MISMATCH"}, status=400)

            if Account.objects.filter(email=email).exists():
                return JsonResponse({"message": "USER_ALREADY_EXISTS"}, status=409)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            Account.objects.create(
                username=username,
                email=email,
                password=hashed_password.decode("utf-8"),
                phone_number=phone_number,
                date_of_birth=date_of_birth,
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email = data["email"]
            password = data["password"]
            if not Account.objects.filter(email=email, password=password).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
