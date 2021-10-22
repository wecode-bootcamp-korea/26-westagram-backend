from django.urls import path
from users.views import UserView

urlpatterns = [
    path('/signup', UserView.as_view())
]