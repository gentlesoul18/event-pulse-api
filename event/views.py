from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from event.serializers import EventSerializer
from event.models import Event

# Create your views here.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_event(request):
    user = request.user
    if user.user_type != "O":
        return Response({"message": "you dont have access to this endpoint"}, status=status.HTTP_403_FORBIDDEN)
    data = request.data
    serializer = EventSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request):
    user = request.user
    if user.user_type != 'A':
        return Response({"message": "you dont have access to this endpoint"}, status=status.HTTP_403_FORBIDDEN)
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status.HTTP_200_OK)