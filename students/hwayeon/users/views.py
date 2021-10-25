# Create your views here.
import json
import re

from django.http import JsonResponse
from django.views import View

from .models import User

email_Validation = re.compile('^[\w+-]+@[\w]+\.[\w.]+$')
password_Validation = re.compile('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*-+_=?]).{8,}$')

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        username = data['name']
        email = data['email']
        password = data['password']
        phone_number = data['phone']

        if username == '' or password == '' :
            return JsonResponse({"message": "Key_Error"}, status=400)

        if not email_Validation.match(email):
            return JsonResponse({"message": "Email_Validation_Error"}, status=400)

        if not password_Validation.match(password):
            return JsonResponse({"message": "Password_Validation_Error"}, status=400)

        if User.objects.filter(email = data['email']).exists():
            return JsonResponse({"message": "Email_Exist_Error"}, status=400)

        User.objects.create(
            username = username,
            email = email,
            password = password,
            phone_number = phone_number
        )

        return JsonResponse({"message": "SUCCESS"}, status=201)