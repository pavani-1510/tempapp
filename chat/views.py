# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import *
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.views.decorators.http import require_POST

# views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def user_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=profile_user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'user_profile.html', context)


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
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_list(request):
    current_user = request.user
    users = User.objects.exclude(id=current_user.id)
    return render(request, 'user_list.html', {'users': users, 'current_user': current_user})


@login_required
def chat_with_user(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    # Fetch or create chat background record if needed (can be removed if not used)

    if request.method == 'POST':
        if 'message' in request.POST:
            message_content = request.POST.get('message')
            if message_content:
                Message.objects.create(sender=request.user, receiver=other_user, content=message_content)
            return redirect('chat_with_user', user_id=user_id)

    # Fetch messages between current user and other user
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)).order_by('timestamp')
    messages_by_date = messages.annotate(date=TruncDate('timestamp')).values('date').distinct()

    context = {
        'other_user': other_user,
        'messages': messages,
        'messages_by_date': messages_by_date,
    }

    return render(request, 'chat_with_user.html', context)


@login_required
@require_POST
def send_message(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    content = request.POST.get('message', '')
    Message.objects.create(sender=request.user, receiver=other_user, content=content)
    return redirect('chat_with_user', user_id=user_id)


@login_required
def delete_all_messages(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to perform this action.")
    Message.objects.all().delete()
    return redirect('home')


@login_required
def fetch_messages(request, receiver_id):
    other_user = get_object_or_404(User, pk=receiver_id)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)).order_by('timestamp')
    messages_data = [{'content': message.content, 'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                      'sender': message.sender.username} for message in messages]
    return JsonResponse({'messages': messages_data})
