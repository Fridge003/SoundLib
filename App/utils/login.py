
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from App.models import User

from .index import render_index

def render_login(request,
    login_failed=False,
    register_failed=False,
    register_nonconsistency=False,
    register_used_name=False,
    ) :
    context          = {}
    context['hello'] = 'PKUpiano Sound Library!'
    context['register_nonconsistency'] = register_nonconsistency
    context['register_used_name'] = register_used_name
    context['register_failed'] = register_failed
    context['login_failed'] = login_failed
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

def process_register_form(request, name, email, password, password2, introduction="Empty") :

    try:
        user = User.objects.create_user(name, email, password, introduction)
    except IntegrityError as e:
        print("Some error occured!", e)
        return render_login(request, register_failed=True, register_used_name=True)
    
    if password != password2 :
        return render_login(request, register_failed=True, register_nonconsistency=True)

    if user is not None:
        user.save()
        return process_login_form(request, name, password)
    else :
        return render_login(request, register_failed=True)