from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Code Challenge Imports
import random
import string
import base64
import hashlib

from users.models import Profile


# Create your views here.
class FitbitAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def construct_access_url(self, user_id):
        client_id = "23R5PJ"

        code_verifier = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
        code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

        code_challenge = hashlib.sha256(code_verifier).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

        base_url = "https://www.fitbit.com/oauth2/authorize?response_type=code"
        client_url = "&client_id={}".format(client_id)
        scope_url = "&scope=activity+cardio_fitness+electrocardiogram+heartrate+location+nutrition+oxygen_saturation" \
                    "+profile+respiratory_rate+settings+sleep+social+temperature+weight"
        code_challenge_url = "&code_challenge={}&code_challenge_method=S256".format(code_challenge)
        state_redirect_url = "&state={}&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Ffitbit%2Fhandle-redirect%2F".format(
            user_id)

        # url = "https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={}&scope=activity+cardio_fitness+electrocardiogram+heartrate+location+nutrition+oxygen_saturation+profile" \
        #       "+respiratory_rate+settings+sleep+social+temperature+weight&code_challenge={}&code_challenge_method=S256&state=4&redirect_uri=http%3A%2F%2F127.0" \
        #       ".0.1%3A8080%2F".format(client_id, code_challenge)

        return base_url + client_url + scope_url + code_challenge_url + state_redirect_url

    def post(self, request):
        user_id = request.auth.payload["user_id"]
        url = self.construct_access_url(user_id)

        content = {'access_url': url}
        return Response(content)


@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def handle_redirect(request):
    if request.method == 'GET':
        code = request.query_params['code']
        user_id = request.query_params['state']

        # Save this code User's Profile
        user = User.objects.filter(id=user_id).first()
        profile = Profile.objects.filter(user=user).first()
        profile.fitbit_auth_code = code
        profile.save()

        return Response({
            "msg": "You Reached Me, {}!!!".format(user.first_name)
        })


# Todo: Rebase common use cases along Web Controller and Scheduler (Keep it Dryyyyyyyyyyyyyyyyyy)
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def fitbit_login(request):
    user_id = request.auth.payload["user_id"]
    profile = Profile.objects.filter(user__id=user_id).first()
    auth_code = profile.fitbit_auth_code


