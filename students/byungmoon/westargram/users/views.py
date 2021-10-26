from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from users.models     import User
import json, re
# Create your views here.
class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data['name']
            email = data['email']
            password = data['password']
            contact = data['contact']
            Other_Personal_Inf = data['Other_Personal_Inf']
            
            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EMAIL_EXISTS"}, status=400)

            User.objects.create(
                name = name,
                email = email,
                password = password,
                contact = contact,
                Other_Personal_Inf = Other_Personal_Inf
            )
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError:
                return JsonResponse({"error_message" : "KEY_ERROR"}, status = 400)