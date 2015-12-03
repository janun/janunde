from django.conf.urls import url
from .views import index, page

urlpatterns = [
    url(r'^$', index),
    url(r'^([\w/]+)', page),
]
