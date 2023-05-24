from django.contrib.auth.models import User, Group
from .models import Hackathon, Submission
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ['id','title', 'description', 'start_date', 'end_date', 'background_image', 'image', 'reward', 'type', 'creator','created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id','user', 'hackathon', 'name', 'summary']