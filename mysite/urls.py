"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from user import views as uv

urlpatterns = [
    url(r'^chat/', include('chat.urls')),
    url(r'^$', uv.login),
    url(r'^logout/$', uv.logout),
    url(r'^register/$', uv.register),
    url(r'^userprofile/(?P<username>[^/]+)/$', uv.userprofile, name='userprofile'),
    url(r'^(?P<username>[^/]+)/friendprofile/(?P<friendname>[^/]+)/$', uv.friendprofile, name='friendprofile'),
    url(r'^(?P<username>[^/]+)/$', uv.back2chat, name='back2chat'),
    url(r'^admin/', admin.site.urls),
]
