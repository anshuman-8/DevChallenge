from rest_framework import response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny


def auth_verify(function):
    @authentication_classes([TokenAuthentication])
    @permission_classes([AllowAny])
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return response.Response({"error": "Not a valid user"})

    return wrap
