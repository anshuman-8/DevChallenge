from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework import viewsets, response, request
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


@api_view(["GET"])
@auth_verify
def userDetail(request):
    try:
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return response.Response(serializer.data)
    except User.DoesNotExist:
        return response.Response({"error": "User does not exist"})
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["POST"])
@permission_classes([AllowAny])
def registerUser(request):
    try:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
    except Exception as e:
        return response.Response({"error": "User not registered", "message": str(e)})


@api_view(["GET"])
def getHackathons(request):
    try:
        hackathons = Hackathon.objects.all()
        serializer = HackathonSerializer(hackathons, many=True)
        return response.Response(serializer.data)
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["GET"])
def getHackathon(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        serializer = HackathonSerializer(hackathon)
        return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["GET"])
@auth_verify
def getRegisteredHackathons(request):
    try:
        hackathons = Hackathon.objects.filter(participants=request.user)
        serializer = HackathonSerializer(hackathons, many=True)
        return response.Response(serializer.data)
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})

@api_view(["GET"])
@auth_verify
def getUserSubmissions(request):
    try:
        submissions = Submission.objects.filter(user=request.user)
        serializer = SubmissionSerializer(submissions, many=True)
        return response.Response(serializer.data)
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["POST"])
@csrf_exempt
@auth_verify
def createHackathon(request):
    request.data["creator"] = request.user.id
    try:
        serializer = HackathonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["PUT"])
@auth_verify
def updateHackathon(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        request.data["creator"] = request.user.id
        if hackathon.type != request.data["type"]:
            return response.Response(
                {"error": "User not allowed to change the type of hackathon"}
            )
        serializer = HackathonSerializer(hackathon, data=request.data)
        if hackathon.creator == request.user:
            if serializer.is_valid():
                serializer.save()
                return response.Response(serializer.data)
            else:
                return response.Response(serializer.errors)
        else:
            return response.Response(
                {"error": "User are not allowed to update this hackathon"}
            )
    except Hackathon.DoesNotExist:
        return response.Response(
            {"error": "Hackathon does not exist or something went wrong"}
        )
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["POST"])
@auth_verify
def joinHackathon(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        if hackathon.creator != request.user:
            hackathon.participants.add(request.user)
            return response.Response({"success": "Joined hackathon successfully"})
        else:
            return response.Response(
                {"error": "You are not allowed to join your own hackathon"}
            )
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["POST"])
@auth_verify
def makeSubmission(request, hackathon_id):
    try:
        hackathon = Hackathon.objects.get(id=hackathon_id)
        if hackathon.participants.filter(id=request.user.id).exists() != False:
            if (
                (hackathon.type == "image" and "image" in request.data)
                or (hackathon.type == "file" and "file" in request.data)
                or (hackathon.type == "link" and "link" in request.data)
            ):
                request.data["hackathon"] = hackathon.id
                request.data["user"] = request.user.id
                serializer = SubmissionSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response(
                        {"success": "Submission made successfully"}
                    )
                else:
                    return response.Response(serializer.errors)
            else:
                return response.Response(
                    {"error": "Invalid submission type or missing required data"}
                )
        else:
            return response.Response(
                {"error": "User not allowed to make submission for this hackathon"}
            )

    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})


@api_view(["GET"])
def getSubmissions(request, hackathon_id):
    try:
        submissions = Submission.objects.filter(hackathon=hackathon_id)
        serializer = SubmissionSerializer(submissions, many=True)
        return response.Response(serializer.data)
    except Hackathon.DoesNotExist:
        return response.Response({"error": "Hackathon does not exist"})
    except Exception as e:
        return response.Response({"error": "Something went wrong", "message": str(e)})
