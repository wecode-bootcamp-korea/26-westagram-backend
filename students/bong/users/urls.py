from django.urls import path
from .views import SignupView

urlpatterns = [
    path("Signup", SignupView.as_view()),
]
