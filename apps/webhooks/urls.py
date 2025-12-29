from django.urls import path
from .views.dashboard import dashboard
from .views.simulator import create_event
from .views.receiver import webhook_receiver

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("create-event/", create_event, name="create_event"),
    path("receiver/", webhook_receiver, name="webhook_receiver"),
]
