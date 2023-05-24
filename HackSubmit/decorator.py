from rest_framework import response


def login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return response.Response({"error": "Not a valid user"})

    return wrap
