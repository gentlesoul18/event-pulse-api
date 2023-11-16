from django.shortcuts import render
from django.db.models import Q

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
    date = request.GET.get(
        "date",
    )
    location = request.GET.get("location", None)
    event_type = request.GET.get("event_type", None)
    if user.user_type == "At":
        return Response(
            {"message": "you dont have access to this action"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if not (date and event_type and request):
        events = Event.objects.all().filter(is_deleted=False)
    elif date and event_type and location:
        events = Event.objects.all().filter(
            date=date, event_type=event_type, location=location, is_deleted=False
        )
    elif (event_type and location) or (event_type and date) or (date and location):
        events = Event.objects.all().filter(
            Q(event_type=event_type, location=location)
            | Q(date=date, location=location)
            | Q(date=date, event_type=event_type),
            is_deleted=False,
        )
    elif event_type or location or date:
        events = Event.objects.all().filter(
            Q(date=date) | Q(event_type=event_type) | Q(location=location),
            is_deleted=False,
        )

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_event(request, id):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "Yous dont have access to this action"},
            status=status.HTTP_403_FORBIDDEN,
        )
    try:
        event = Event.objects.get(id=id, is_deleted=False)
    except Event.DoesNotExist:
        return Response(
            {"message": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = EventSerializer(event)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_event(request, id):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "You dont have access to this action"},
            status.HTTP_403_FORBIDDEN,
        )
    data = request.data
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(
            {"message": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = EventSerializer(event, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_206_PARTIAL_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_event(request, id):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "You dont have access to this action"},
            status.HTTP_403_FORBIDDEN,
        )
    try:
        event = Event.objects.get(id=id, is_deleted=False)
    except Event.DoesNotExist:
        return Response(
            {"message": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if event.is_deleted == True:
        return Response(
            {"message": "Event already deleted"}, status.HTTP_208_ALREADY_REPORTED
        )
    event.is_deleted = True
    event.save()
    return Response({"message": "Event Deleted"}, status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def verify_event(request, id):
    user = request.user
    if user.user_type != "A":
        return Response(
            {"message": "You dont have access to perform this action"},
            status.HTTP_403_FORBIDDEN,
        )
    try:
        event = Event.objects.get(id=id, is_deleted=False)
    except Event.DoesNotExist:
        return Response(
            {"message": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if event.is_verified == True:
        return Response(
            {"message": "Event already verified"}, status.HTTP_208_ALREADY_REPORTED
        )
    event.is_verified = True
    event.save()
    return Response({"message": "Event verified"}, status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def restore_event(request, id):
    user = request.user
    if user.user_type == "At":
        return Response(
            {"message": "You dont have access to this action"},
            status.HTTP_403_FORBIDDEN,
        )
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(
            {"message": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if event.is_deleted == False:
        return Response(
            {"message": "Event not deleted"}, status.HTTP_208_ALREADY_REPORTED
        )
    event.is_deleted = False
    event.save()
    return Response({"message": "Event restored"}, status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def search_event(request):
    event = Event.objects.get(id=id)
    pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_verified_events(request):
    user = request.user
    if user.user_type != "A":
        return Response(
            {"message": "You dont have access to perform this action"},
            status.HTTP_403_FORBIDDEN,
        )
    events = Event.objects.all().filter(is_verified=True)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_deleted_events(request):
    user = request.user
    if user.user_type != "A":
        return Response(
            {"message": "You dont have access to perform this action"},
            status.HTTP_403_FORBIDDEN,
        )
    events = Event.objects.all().filter(is_deleted=True)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status.HTTP_200_OK)
