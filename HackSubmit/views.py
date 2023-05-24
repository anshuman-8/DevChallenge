from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, response, request
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Hackathon, Submission, User
from .serializers import (
    HackathonSerializer,
    UserSerializer,
    RegisterSerializer,
    SubmissionSerializer,
)
from .decorator import login_required


class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = HackathonSerializer


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(["GET"])
def getHackathons(request):
    hackathons = Hackathon.objects.all()
    serializer = HackathonSerializer(hackathons, many=True)
    return response.Response(serializer.data)


@api_view(["GET"])
def getHackathon(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        serializer = HackathonSerializer(hackathon)
        return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})


@login_required
@api_view(["POST"])
def createHackathon(request):
    print("data", request.data)
    print("user", request.user)
    print("is auth", request.user.is_authenticated)
    print("is staff", request.user.is_staff)
    print("request Data: ", request.data)
    serializer = HackathonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creator=request.user)
        return response.Response(serializer.data)
    else:
        return response.Response(serializer.errors)


@login_required
@api_view(["POST"])
def updateHackathon(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        serializer = HackathonSerializer(data=request.data)
        if hackathon.creator == request.user:
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data)
            else:
                return response.Response(serializer.errors)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})


@api_view(["GET"])
def getHackathon(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        serializer = HackathonSerializer(hackathon)
        return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})


@login_required
@api_view(["POST"])
def makeSubmission(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hackathon=hackathon, user=request.user)
            return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})
