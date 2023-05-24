from django.shortcuts import render
from django.urls import path
from . import views

urlpatterns = [
    path('hackathons/', views.getHackathons, name='getHackathons'),
    # path('hackathon/create',views.createHackathon, name='Create Hackathon'),
    # path('hackathon/<int:hackathon_id>', views.getHackathon, name='Get Hackathon'),
    # path('hackathon/<int:hackathon_id>/update', views.updateHackathon, name='Update Hackathon'),
    # path('hackathon/<int:hackathon_id>/submit', views.makeSubmission, name='Make Submission')
]