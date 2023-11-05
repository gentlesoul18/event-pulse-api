from django.forms import ValidationError
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from authentication.serializers import SocialLoginSerializer, RegisterSerializer, UserSerializer
from authentication.models import User
from authentication.exceptions import AccountNotRegisteredException
from authentication.utils import get_facebook_user_info, user_get_or_create, jwt_login, get_google_user_info


# Create your views here.
@api_view(['GET'])
def landing_page(request):
    return Response({"message": "This is the landing Page of Event Pulse API"})


class FacebookLogin(APIView):
    serializer_class = SocialLoginSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """
        auth_token = request.data["auth_token"]
        
        user_data = get_facebook_user_info(access_token=auth_token)
        email = user_data.get("email")
        name = user_data.get("name").split(" ")
        first_name = name[0]
        last_name = name[1]
        user = user_get_or_create(email, first_name, last_name)

        response = Response()
        token = jwt_login(response=response, user=user)
        response.data = {**user_data, "token": token}
        return response
    

class GoogleLogin(APIView):
    """
    Google Login View to log user in with just a click
    parameter needed: code sent to google from frontend
    The code is used to generate users access token then the access token,
    the access token is then used to generate the user's data from google
    """

    serializer_class = SocialLoginSerializer

    def post(self, request):
        code = request.data["auth_token"]
        user_data = get_google_user_info(access_token=code)
        
        email = user_data["email"]
        first_name = user_data["given_name"]
        last_name = user_data["family_name"]

        user = user_get_or_create(email, first_name, last_name)

        response = Response()
        token = jwt_login(response=response, user=user)
        response.data = {**user_data, "token": token}
        return response


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()
    user_data = serializer.data
    user = User.objects.get(email=user_data["email"])
    token = user.token()
    response = Response()
    response.data = {**user_data, "access_token": token}
    return response


@api_view(['POST'])
def sign_in(request):
    username = request.data["username"]
    password = request.data["password"]
    try:
        user = User.objects.get(Q(username=username.lower()) | Q(email=username))
    except AccountNotRegisteredException as e:
        raise e.default_detail
        # raise ValidationError({"message": "This user does not exist"})

    if not user.check_password(password):
        raise ValidationError({"message": "Incorrect Password!"})

    serializer = UserSerializer(user)

    response = Response()
    token = user.token()
    response.set_cookie(
        key="jwt", value=token, httponly=True
    )  # creates cookies for user session
    response.data = {"access_token": token, **serializer.data}
    return response