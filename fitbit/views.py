from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


# Create your views here.
class FitbitAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.auth.payload["user_id"]
