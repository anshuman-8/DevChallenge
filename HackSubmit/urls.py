from django.urls import path
from django.shortcuts import render
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    # auth
    path("register/", views.registerUser, name="Register"),
    path("login/", obtain_auth_token, name="login auth-token"),

    # User apis
    path("user/", views.userDetail, name="User details"),
    path("myHackathons/", views.getRegisteredHackathons, name="Get User's Hackathons"),
    path("mySubmissions/", views.getUserSubmissions, name="Get User's Submissions"),

    # Hackathon apis
    path("hackathons/", views.getHackathons, name="Get Hackathons"),
    path("hackathon/create", views.createHackathon, name="Create Hackathon"),
    path("hackathon/<int:hackathon_id>", views.getHackathon, name="Get Hackathon"),
    path("hackathon/<int:hackathon_id>/update",views.updateHackathon,name="Update Hackathon",),
    path("hackathon/<int:hackathon_id>/join", views.joinHackathon, name="Get Hackathon"),

    # Submission apis
    path("hackathon/<int:hackathon_id>/submit",views.makeSubmission, name="Make Submission",),
    path("hackathon/<int:hackathon_id>/submissions", views.getSubmissions, name="Get Submissions",)
]
