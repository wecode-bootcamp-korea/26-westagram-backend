from django.urls import path

from .views import LogInView, UserListView

urlpatterns = [
    path("/signup", UserListView.as_view()),
    path("/login", LogInView.as_view())
]