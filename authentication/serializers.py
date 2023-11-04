from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    """Handles serialization of social logins related data"""
    auth_token = serializers.CharField()
