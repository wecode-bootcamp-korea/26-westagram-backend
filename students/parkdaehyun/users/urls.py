from django.urls               import path
from django.urls.resolvers import URLPattern
from django.views.generic.base import View
from .views                    import UserlistView


urlpatterns = [
    path("user", UserlistView.as_view())
]