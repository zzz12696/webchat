from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<room_name>[^/]+)/(?P<user_name>[^/]+)/$', views.room, name='room'),
]
