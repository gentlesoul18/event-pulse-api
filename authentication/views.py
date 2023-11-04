from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import SocialLoginSerializer
from authentication.utils import get_facebook_user_info, user_get_or_create, jwt_login, get_google_user_info


# Create your views here.
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
