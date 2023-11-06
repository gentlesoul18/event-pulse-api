from django.shortcuts import render

from rest_framework.decorators import api_view

from event.serializers import EventSerializer
# Create your views here.
@api_view(['POST'])
def create_event(request):
    data = request.data
    