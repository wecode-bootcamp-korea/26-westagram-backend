from django.urls import path

from .views import UserListView

urlpatterns = [
    path("/us", UserListView.as_view())
]