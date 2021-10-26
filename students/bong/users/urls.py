from django.urls import path
from .views import SignupView, LoginView

urlpatterns = [
    path("user/signup", SignupView.as_view()),
    path("user/login", LoginView.as_view()),
]
