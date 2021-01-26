from login.models import Login, LoginInfo
from django.shortcuts import render_to_response


def signup(request):
    params = {}
    return render_to_response('login/signup.html', 
                              params,
                              context_instance = RequestContext(request))

