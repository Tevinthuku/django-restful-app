from django.conf.urls import url
from .views import (UpdateModelDetailApiView, UpdateModelListApiView)

urlpatterns = [
    url(r'^$', UpdateModelListApiView.as_view()),
    url(r'^(?P<id>\d+)/$', UpdateModelDetailApiView.as_view())
]
