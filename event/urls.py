from django.urls import path
from event import views

urlpatterns = [
    path('create', views.create_event, name='create'),
    path('', views.get_events, name="get-events"),
]
