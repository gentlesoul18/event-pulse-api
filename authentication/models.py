from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


# Create your models here.
class User(AbstractUser):
    USER_TYPE = (
        ("A", "Admin"),
        ("O", "Organizer"),
        ("At", "Attendee"),
    )
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(
        max_length=2, choices=USER_TYPE, default=USER_TYPE[2], null=True, blank=True
    )
    

    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return self.username

    def decouple_username(self):
        splitted_username = self.username.split(":")
        return splitted_username[0]

    def token(self):
        access = AccessToken.for_user(self)
        return str(access)
