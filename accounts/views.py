from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
import sys
from accounts.authentication import PersonaAuthenticationBackend

def login(request):
    print('login view', file=sys.stderr)
    #user = PersonaAuthenticationBackend().authenticate(request.POST['assertion'])
    user = authenticate(assertion=request.POST['assertion'])
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')

