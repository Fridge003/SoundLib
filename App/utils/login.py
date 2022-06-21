
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from App.models import User

from .index import render_index

# Render the "login" page
# Parameters include error messages when login or registration fails
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

# Process a login form
def process_login_form(request, name, password) :

    user = authenticate(request, username=name, password=password)

    if user is not None:
        # login success
        login(request, user)
        return True
    else :
        # login failed
        return {"login_failed": True}

# Process a registration form
def process_register_form(request, name, email, password, password2, introduction="Empty") :

    try:
        user = User.objects.create_user(name, email, password, introduction)
    except IntegrityError as e: # Possibly conflict username
        return {"register_failed":True, "register_used_name":True, "register_nonconsistency":False}
    
    if password != password2 :
        return {"register_failed":True, "register_used_name":False, "register_nonconsistency":True}

    if user is not None:
        user.save()
        res = process_login_form(request, name, password)
        if res == True :
            return {"register_failed":False, "register_used_name":False, "register_nonconsistency":False}
        else :  # Not quite possible: registration successes but login failed
            return {"register_failed":True, "register_used_name":False, "register_nonconsistency":False}
    else :      # Not quite possible: nothing returned in creating the user
        return {"register_failed":True, "register_used_name":False, "register_nonconsistency":False}