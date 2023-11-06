from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','user','title', 'description', 'event_type', 'date', 'time', 'location', 'created_on', 'updated_on']
        extra_kwargs = {
            'user': {'read_only': True},
            'created_on': {'read_only': True},
            'updated_on': {'read_only': True}
        }