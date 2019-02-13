from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django_talk.models import ChatRoom


class IndexView(View):
    def get(self, request):
        user = False
        user_id = request.session.get('_auth_user_id')
        rooms = ChatRoom.objects.all()
        if user_id:
            user = User.objects.get(id=user_id)
        return render(request, 'index.html', {
            "user": user,
            'rooms': rooms,
        })


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        usr = request.POST.get('username', '')
        psw = request.POST.get('password', '')
        callback = ''
        try:
            login(request, user=authenticate(username=usr, password=psw))
            return redirect('index')
        except:
            callback = '用户名或密码错误'
            return render(request, 'login.html', {
                'callback': callback,
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class RegistView(View):
    def get(self, request):
        return render(request, 'register.html', {})

    def post(self, request):
        usr = request.POST.get('username', '')
        psw = request.POST.get('password', '')
        cfm = request.POST.get('confirm', '')
        callback = ''

        import re
        err = ''
        errors = [
            '只能使用大小写字母、数字与下划线' if re.match("[^a-zA-Z0-9_]+", usr + psw) else '',
            '用户名已存在' if User.objects.filter(username=usr) else '',
            '用户名必须小于20个字' if len(usr) > 20 else '',
            '用户名为空' if len(usr) <= 0 else '',
            '密码必须小于30个字' if len(psw) > 30 else '',
            '密码为空' if len(psw) <= 0 else '',
            '两次密码输入不一致' if psw != cfm else ''
        ]
        for error in errors:
            if errors.index(error) > 3:
                callback = usr
            if error != '':
                err = error
                break
        
        if len(err) == 0:
            try:
                new_user = User(username=usr)
                new_user.set_password(psw)
                new_user.save()
                return redirect('login')
            except:
                return render(request, 'register.html', {
                    'error': '未知错误',
                })
        else:
            return render(request, 'register.html', {
                'error': err,
                'callback': callback,
            })


class UserView(View):
    def get(self, request):
        try:
            user = User.objects.get(id=request.session['_auth_user_id'])
            return render(request, 'user.html', {
                'username': user.username,
                'email': user.email
            })
        except:
            return render(request, 'user.html', {
                'username': '',
                'email': ''
            })
