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


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    
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


@api_view(["PUT"])
@auth_verify
def updateHackathon(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        request.data["creator"] = request.user.id
        if hackathon.type != request.data["type"]:
            return response.Response({"error": "You are not allowed to change the type of hackathon"}) 
        serializer = HackathonSerializer(hackathon, data=request.data)
        if hackathon.creator == request.user:
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data)
            else:
                return response.Response(serializer.errors)
        else:
            return response.Response({"error": "You are not allowed to update this hackathon"})
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist or something went wrong"})


@api_view(["POST"])
@auth_verify
def makeSubmission(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        request.data['hackathon'] = hackathon.id
        request.data["user"] = request.user.id
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})


@api_view(["GET"])
def getSubmissions(request,hackathon_id):
    try:
        submissions = Submission.objects.filter(
            hackathon=hackathon_id
        )
        serializer = SubmissionSerializer(submissions, many=True)
        return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})
