from django.db import models
from authentication.models import User
# Create your models here.

class Event(models.Model):
    EVENT_TYPE = (
        ('E', 'Entertainment'),
        ('S', 'Seminar'),
        ('C', 'Conference'),
        ('R', 'Religious'),
        ('W', 'Workshop'),
        ('H', 'Hackathon'),
        ('O', 'Other')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    event_type = models.CharField(max_length=1, choices=EVENT_TYPE, default=EVENT_TYPE[2])
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title