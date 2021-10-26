from django.urls               import path

from .views                    import Login, UserlistView

urlpatterns = [
    path("user", UserlistView.as_view()),
    path("/login", Login.as_view())
]