"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework.permissions import AllowAny

from happyApp.views import Users, User, Happy, Teams, TeamRedactor, AddTeamMemmber, TeamMoodMark, TeamsMoodMark
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', Users.as_view(permission_classes=[AllowAny])),
    path('user/<int:pk>/', User.as_view()),
    path('user/<int:user_id>/happiness/', Happy.as_view()),
    path('team/', Teams.as_view(actions={'get': 'list', 'post': 'create'})),
    path('team/<int:pk>/', Teams.as_view(actions={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('team/<int:id>/memmbers/', TeamRedactor.as_view()),
    path('team/<int:id>/memmbers/<int:pk>/', AddTeamMemmber.as_view()),
    path('team/<int:id>/mood_mark/', TeamMoodMark.as_view()),
    path('teams/mood_mark/', TeamsMoodMark.as_view(permission_classes=[AllowAny])),
    # path('', create_user)
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
