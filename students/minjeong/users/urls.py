from django.urls import path
from .views      import UserView

urlpatterns = [
    path('/signup', UserView.as_view()),
]
