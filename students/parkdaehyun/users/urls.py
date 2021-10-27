from django.urls               import path

from .views                    import LoginView, UserlistView

urlpatterns = [
    path("/user", UserlistView.as_view()),
    path("/login", LoginView.as_view())
]