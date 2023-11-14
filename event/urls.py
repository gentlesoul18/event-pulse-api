from django.urls import path
from event import views

urlpatterns = [
    path('create', views.create_event, name='create'),
    path('', views.get_events, name="get-events"),
    path('<int:id>', views.get_event, name="get-event"),
    path('update/<int:id>', views.update_event, name="update-event"),
    path('delete/<int:id>', views.delete_event, name="delete-event"),
    path('restore/<int:id>', views.restore_event, name="restore-event"),
    path('verify/<int:id>', views.verify_event, name="verify-event"),
]
