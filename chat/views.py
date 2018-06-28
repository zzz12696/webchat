from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from user.models import User


def room(request, room_name, user_name):
    room_name_json = mark_safe(json.dumps(room_name))
    user_name_json = mark_safe(json.dumps(user_name))

    users_online = User.objects.filter(is_login=1)
    users_offline = User.objects.filter(is_login=0)
    return render(request, 'chat/room.html', {
        'room_name_json': room_name_json,
        'user_name_json': user_name_json,
        'roomname': room_name,
        'username': user_name,
        'users_online': users_online,
        'users_offline': users_offline,
    })
