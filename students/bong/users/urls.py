from django.urls import path
from .views import UserView #, LoginView

urlpatterns = [
    path("User", UserView.as_view()),
    #path("User", LoginView.as_view()),
]
