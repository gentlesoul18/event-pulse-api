from django.urls import path
from authentication import views

urlpatterns = [
    path('google', views.GoogleLogin.as_view(), name="google-login"),
    path('facebook', views.FacebookLogin.as_view(), name="facebook-login"),
    path('register', views.register_user, name="register"),
    path('signin', views.sign_in, name="signin"),
]