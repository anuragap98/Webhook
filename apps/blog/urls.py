from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .models import LogMessage

home_and_log_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[
        :5
    ],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="blog/home.html",
)

urlpatterns = [
    path("", home_and_log_view, name="home"),
    path("contact/", views.contact, name="contact"),
    path("log/", views.log_message, name="log"),
]

urlpatterns += staticfiles_urlpatterns()
