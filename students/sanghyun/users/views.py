from django.http        import JsonResponse
from django.views       import View
from users.models       import User
import json, re

class SignUpView(View):
    def post(self, request):
        try:        
            data        = json.loads(request.body)
            name        = data['name']
            password    = data['password']
            birth       = data['birth']
            email       = data['email']
            mobile      = data['mobile']
            sns_address = data['sns_address']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EMAIL_EXISTS"}, status=409)

            User.objects.create(
                name        = name,
                password    = password,
                birth       = birth,
                email       = email,
                mobile      = mobile,
                sns_address = sns_address,
            )
            return JsonResponse({'MESSAGE':'CREATED'}, status=201)
        except:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400) 
