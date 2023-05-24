from django.urls import path
from django.shortcuts import render
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path("register/", views.RegisterUserAPIView.as_view()),
    path("login/", obtain_auth_token, name="login auth-token"),
    path("user/", views.UserDetailAPI.as_view()),
    
    path("hackathons/", views.getHackathons, name="Get Hackathons"),
    path("hackathon/create", views.createHackathon, name="Create Hackathon"),
    path("hackathon/<int:hackathon_id>", views.getHackathon, name="Get Hackathon"),
    # path('hackathon/<int:hackathon_id>/update', views.updateHackathon, name='Update Hackathon'),
    path("hackathon/<int:hackathon_id>/submit",views.makeSubmission,name="Make Submission",),
]
