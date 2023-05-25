from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import viewsets, response, request
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from .models import Hackathon, Submission, User
from .serializers import (
    HackathonSerializer,
    UserSerializer,
    RegisterSerializer,
    SubmissionSerializer,
)
from .decorator import auth_verify


class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = HackathonSerializer

    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def userDetail(request):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return response.Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
    except Exception as e:
        return response.Response({"error":"User not registered", "message":str(e)})


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


@api_view(["POST"])
@csrf_exempt
@auth_verify
def createHackathon(request):
    request.data["creator"] = request.user.id
    serializer = HackathonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creator=request.user)
        return response.Response(serializer.data)
    else:
        return response.Response(serializer.errors)


@auth_verify
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


@auth_verify
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


@api_view(["GET"])
def getSubmissions(request):
    try:
        submissions = Submission.objects.filter(
            hackathon_id=request.data["hackathon_id"]
        )
        serializer = SubmissionSerializer(submissions, many=True)
        return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})
