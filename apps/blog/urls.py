from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("blog/", views.BlogListView.as_view(), name="blog"),
    path("blog_message/", views.blog_message, name="blog_message"),
]

urlpatterns += staticfiles_urlpatterns()
