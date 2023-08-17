from django.urls import path
from . import views
from .views import RegisterApi, HelloView

urlpatterns = [
    path("create/", RegisterApi.as_view()),
    path("hello/", HelloView.as_view())
]