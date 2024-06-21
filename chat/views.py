from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from .models import Message
from django.views.decorators.http import require_POST


def home(request):
    if request.user.is_authenticated:
        return redirect('user_list')
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_list')
    return render(request, 'main/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message

def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def chat_with_user(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(sender=request.user, receiver=other_user) | Message.objects.filter(sender=other_user, receiver=request.user)
    return render(request, 'chat_with_user.html', {'other_user': other_user, 'messages': messages})

def send_message(request, user_id):
    if request.method == 'POST':
        other_user = get_object_or_404(User, pk=user_id)
        content = request.POST.get('message', '')
        message = Message(sender=request.user, receiver=other_user, content=content)
        message.save()
    return redirect('chat_with_user', user_id=user_id)
