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
    if user.user_type == "At":
        return Response(
            {"message": "you dont have access to this action"},
            status=status.HTTP_403_FORBIDDEN,
        )
    data = request.data
    serializer = EventSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_events(request):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "you dont have access to this action"},
            status=status.HTTP_403_FORBIDDEN,
        )
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_event(request):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "Yo dont have access to this action"},
            status=status.HTTP_403_FORBIDDEN,
        )
    id = request.GET.get("id")
    event = Event.objects.get(id=id).filter(active=True)
    serializer = EventSerializer(event)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_event(request):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "You dont have access to this action"},
            status.HTTP_403_FORBIDDEN,
        )
    data = request.body
    id = data["id"]
    event = Event.objects.get(id=id)
    serializer = EventSerializer(event, data=data, partial=True)
    return Response(serializer.data, status.HTTP_206_PARTIAL_CONTENT)


@api_view(["DELETE"])
@permission_classes(IsAuthenticated)
def delete_event(request, kwargs):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "You dont have access to this action"},
            status.HTTP_403_FORBIDDEN,
        )
    id = kwargs["id"]
    event = Event.objects.get(id=id)
    if event.is_deleted == True:
        return Response(
            {"message": "Event already deleted"}, status.HTTP_208_ALREADY_REPORTED
        )
    event.is_deleted = True
    event.save()
    return Response({"message": "Event Deleted"}, status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes(IsAuthenticated)
def verify_event(request, kwargs):
    user = request.user
    if user.user_type != "A":
        return Response(
            {"message": "You dont have access to perform this action"},
            status.HTTP_403_FORBIDDEN,
        )
    id = kwargs["id"]
    event = Event.objects.get(id=id)
    if event.is_verified == True:
        return Response(
            {"message": "Event already verified"}, status.HTTP_208_ALREADY_REPORTED
        )
    event.is_verified = True
    event.save()
    return Response({"message": "Event verified"}, status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def restore_event(request, kwargs):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "You dont have access to this action"},
            status.HTTP_403_FORBIDDEN,
        )
    id = kwargs["id"]
    event = Event.objects.get(id=id)
    if event.is_deleted == False:
        return Response(
            {"message": "Event not deleted"}, status.HTTP_208_ALREADY_REPORTED
        )
    event.is_deleted = False
    event.save()
    return Response({"message": "Event restored"}, status.HTTP_204_NO_CONTENT)
