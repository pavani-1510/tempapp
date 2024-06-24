# main/urls.py

from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list, name='user_list'),
    path('chat/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('delete-all-messages/', views.delete_all_messages, name='delete_all_messages'),
    path('fetch-messages/<int:receiver_id>/', views.fetch_messages, name='fetch_messages'),
    path('send-message/<int:user_id>/', views.send_message, name='send_message'),

]
