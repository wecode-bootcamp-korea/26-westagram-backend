from django.urls import path
from .views import UserView

urlpatterns = [
    path("User", UserView.as_view()),
]
