from django.shortcuts import render, redirect
from user.models import User


def login_check(func):
    def inner(request, *args, **kwargs):
        ret = request.session.get('is_login')
        if ret == "1":
            return func(request, *args, **kwargs)
        else:
            return redirect("/")
    return inner


def login(request):
    error_msg = ''
    if request.method == 'POST':
        input_email = request.POST.get('email')
        input_password = request.POST.get('pwd')

        try:
            user_obj = User.objects.get(email=input_email)
        except:
            error_msg = '无此账号'
            return render(request, 'user/login.html', {'error_msg': error_msg})

        if input_password == user_obj.password:
            # 修改session
            request.session['is_login'] = '1'

            user_obj.is_login = 1
            user_obj.save()
            username = user_obj.username

            users_online = User.objects.filter(is_login=1)
            users_offline = User.objects.filter(is_login=0)
            return render(request, 'chat/index.html', {
                'username': username,
                'users_online': users_online,
                'users_offline': users_offline
            })
        else:
            error_msg = '账号或密码错误'
    return render(request, 'user/login.html', {'error_msg': error_msg})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pwd')

        User.objects.create(username=username, email=email, password=password)
        return render(request, 'user/login.html')
    return render(request, 'user/register.html')


def logout(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_obj = User.objects.get(username=username)
        user_obj.is_login = 0
        user_obj.save()
        # 清空session
        request.session.flush()
        return render(request, 'user/login.html')


@login_check
def userprofile(request, username):
    if request.method == 'POST':
        users_online = User.objects.filter(is_login=1)
        users_offline = User.objects.filter(is_login=0)

        email = request.POST.get('email')
        user_obj = User.objects.get(email=email)

        re_password = request.POST.get('re_pwd')
        re_password_2 = request.POST.get('re_pwd_2')

        if re_password == re_password_2:
            user_obj.password = re_password
            user_obj.save()
            message = '密码修改成功'
        else:
            message = '两次密码不一致，修改密码失败'
        return render(request, 'user/userprofile.html', {
            'user_obj': user_obj,
            'users_online': users_online,
            'users_offline': users_offline,
            'message': message,
        })
    if request.method == 'GET':
        try:
            user_obj = User.objects.get(username=username)
        except:
            return redirect('/')

        users_online = User.objects.filter(is_login=1)
        users_offline = User.objects.filter(is_login=0)
        return render(request, 'user/userprofile.html', {
            'user_obj': user_obj,
            'users_online': users_online,
            'users_offline': users_offline,
        })


@login_check
def back2chat(request, username):
    users_online = User.objects.filter(is_login=1)
    users_offline = User.objects.filter(is_login=0)
    return render(request, 'chat/index.html', {
        'username': username,
        'users_online': users_online,
        'users_offline': users_offline,
    })


@login_check
def friendprofile(request, username, friendname):
    user_obj = User.objects.get(username=username)
    fri_obj = User.objects.get(username=friendname)

    users_online = User.objects.filter(is_login=1)
    users_offline = User.objects.filter(is_login=0)
    return render(request, 'user/friendprofile.html', {
        'user_obj': user_obj,
        'fri_obj': fri_obj,
        'users_online': users_online,
        'users_offline': users_offline,
    })