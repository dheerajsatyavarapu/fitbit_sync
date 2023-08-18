from django.urls import path
from .views import FitbitAuth, handle_redirect

urlpatterns = [
    path("fitbit-sync/", FitbitAuth.as_view()),
    path("handle-redirect/", handle_redirect)
]
