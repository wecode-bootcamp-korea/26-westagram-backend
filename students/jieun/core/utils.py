import jwt

from functools        import wraps
from django.http      import JsonResponse
from django.conf      import settings

from users.models     import User
from postings.models  import Posting

def login_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            token         = request.headers.get("Authorization", None)
            payload       = jwt.decode(token, settings.JWT['SECRET'], algorithms=settings.JWT['ALGORITHM'])
            user          = User.objects.get(id=payload["user_id"])
            request.user  = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "USER_DOES_NOT_EXIST"}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper

def posting_existed(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            posting_id = kwargs['id']
            if not Posting.objects.filter(id=posting_id).exists():
                return JsonResponse({"message": f"POSTING(id:{posting_id})_NOT_FOUND"}, status=404)

        except Posting.DoesNotExist:
            return JsonResponse({"message": "POSTING_DOES_NOT_EXIST"}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper