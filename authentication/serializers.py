from rest_framework import serializers

from authentication.exceptions import PlainValidationError
from authentication.models import User

class SocialLoginSerializer(serializers.Serializer):
    """Handles serialization of social logins related data"""
    auth_token = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            )
    username = serializers.CharField(
            required=True,
            )
    user_type = serializers.CharField(default="USER")
    password = serializers.CharField(write_only=True, required=True,)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username',  'email', 'user_type','password', 'confirm_password']
        extra_kwargs = {
            'email':{'unique':True},
            'username':{'unique': True, 'lower': True},
        }


    def validate(self, attrs):
        """ 
        checks if parameters passed in are valid
        e.g Password length, email uniqueness, et.c
        
        """
        
        email_exists = User.objects.filter(email=attrs['email']).exists()
        username_exists = User.objects.filter(username=attrs['username']).exists()
        

        if username_exists:
            raise PlainValidationError({"message":"Username already exist, enter a unique username"})
        elif email_exists:
            raise PlainValidationError({"message":"Email already exist, enter a unique email"})
        elif len(attrs['password']) < 8:
            raise PlainValidationError({"message": "Password too short, it must contain atleast 8 characters!"})
        elif attrs['password'] != attrs['confirm_password']:
            raise PlainValidationError({"message":"Password fields doesn't match."})
        return attrs
    
    def create(self, validated_data):
        username=validated_data['username'].lower()
        email=validated_data['email']
        user_type=validated_data['user_type']
        user = User.objects.create(
            username=username, 
            email=email,
            user_type=user_type
            )

        
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']
        extra_kwargs = {
            'password':{'write_only':True}
        }
