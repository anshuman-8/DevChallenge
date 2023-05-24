from django.shortcuts import render
from rest_framework import viewsets, response, request
from .models import Hackathon, Submission, User
from .serializers import HackathonSerializer
from rest_framework.decorators import api_view


class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = HackathonSerializer


@api_view(["GET"])
def getHackathons(request):
    hackathons = Hackathon.objects.all()
    # print(hackathons)
    serializer = HackathonSerializer(hackathons, many=True)
    return response.Response(serializer.data)


@api_view(["POST"])
def createHackathon(request):
    serializer = HackathonSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
    return response.Response(serializer.data)
