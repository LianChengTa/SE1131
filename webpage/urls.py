"""
URL configuration for SE1131 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import password_edit

urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('mainpage/',views.get_main_page,name='get_main_page'),
    path('detail/<int:event_id>/',views.get_event_detail,name='detail'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('password_edit/',password_edit.as_view(),name="password_edit"),
    path('profile_edit/',views.get_profile_edit,name='profile_edit'),
    path('add_event/',views.get_add_event, name='add_event')
]