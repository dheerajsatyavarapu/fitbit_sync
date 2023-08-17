from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.serialzers import RegisterSerializer, UserSerializer


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.auth.payload["user_id"]
        user = User.objects.get(id=user_id)

        content = {'message': 'Hello, {}'.format(user.first_name)}
        return Response(content)
