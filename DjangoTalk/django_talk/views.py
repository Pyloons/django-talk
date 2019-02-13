from django.shortcuts import render, redirect
from django.views import View


class ChatView(View):
    def get(self, request, room_name):
        if request.user.is_authenticated():
            return render(request, 'chatroom.html', {
                'room_name': room_name,
            })
        else:
            return redirect('login')
