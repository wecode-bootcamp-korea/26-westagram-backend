from django.urls import path

from .views import UserListView

urlpatterns = [
    path("/signup", UserListView.as_view())
]