
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from SoundLib.app.index import render_index

def render_login(request,
    login_failed=False,
    register_failed=False,
    register_nonconsistency=False
    ) :
    context          = {}
    context['hello'] = 'PKUpiano Sound Library!'
    return render(request, 'login.html', context)

def process_login_form(request, name, password) :

    user = authenticate(request, username=name, password=password)

    if user is not None:
        # login success
        login(request, user)
        return render_index(request)
    else :
        # login failed
        return render_login(request, login_failed=True)

def process_register_form(request, name, email, password) :

    user = User.objects.create_user(name, email, password)

    if user is not None:
        user.save()
        return process_login_form(request, name, password)
    else :
        return render_login(request, register_failed=True)