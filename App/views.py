from django.shortcuts import render, redirect
from django import forms
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate, login

import datetime
from App.models import User

from App.utils.index import render_index
from App.utils.login import render_login, process_login_form, process_register_form
from App.utils.upload import process_upload
from App.utils.user import render_user_change, render_user_info, process_change_form
 
 # Index page
def hello(Request):
    
    return render_index(Request)

# User is accesing upload page
# This page needs auth
@login_required
def upload(Request):
    RecordingName = Request.POST['RecordingName']
    ComposerName = Request.POST['ComposerName']
    Description = Request.POST['Description']
    UploadTime = datetime.datetime.now()
    MyFile = Request.FILES['File']
    if Request.method == 'POST' and MyFile:
        process_upload(MyFile, 
            RecordingName=RecordingName,
            ComposerName=ComposerName,
            Description=Description,
            UploadTime=UploadTime,
            UploadUser=Request.user
        )
        return render_index(Request)

    return render_index(Request)

# User is accessing "login" page,
def login(Request):

    if Request.user.is_authenticated:

        return redirect('/user/'+Request.user.username+'/')

    return render_login(Request)

# When user submitted a login form in the "login" page,
# process that form and redirect to main page if successed
def login_form(Request):

    UserName = Request.POST['UserName']
    Password = Request.POST['Password']

    res = process_login_form(Request, UserName, Password)

    if res == True :    # success
        return redirect('/')
    else : # failure
        return render_login(Request, login_failed=True)

# When user submitted a registration form in the "login" page,
# process that from and auto-login if successed
def register_form(Request):

    UserName = Request.POST['UserName']
    Email = Request.POST['Email']
    Password = Request.POST['Password']
    Password2 = Request.POST['Password2']

    res = process_register_form(Request, UserName, Email, Password, Password2)

    if "register_failed" in res : # failed registration
        return render_login(Request,
                            login_failed=False,
                            register_failed=res["register_failed"],
                            register_nonconsistency=res["register_nonconsistency"],
                            register_used_name=res["register_used_name"])
    else :
        return redirect('/')

# Logout a user
def logout(Request) :

    logout_user(Request)

    return render_index(Request)

# Accesing user info page
def user_info(Request, **kwargs) :

    SelectedUsers = User.objects.filter(username=kwargs["username"])

    return render_user_info(Request, Users=SelectedUsers)

# Accesing change page
def user_info_change(Request, **kwards) :

    return render_user_change(Request)

# Comminting a change form
def user_info_change_commit(Request, **kwards) :

    UserName = Request.POST['UserName']
    Email = Request.POST['Email']
    Password = Request.POST['Password']
    Password2 = Request.POST['Password2']
    Introduction = Request.POST['Introduction']

    res = process_change_form(Request, UserName, Email, Password, Password2, Introduction)

    if res == True :    # the user info changed successfully

        print("changed successfully, refreshing...")
        logout_user(Request)
        res = process_login_form(Request, UserName, Password)
        if res == True :    # success
            return redirect('/user/'+Request.user.username+'/')
        else : # failure
            return render_login(Request, login_failed=True)

    else :  # failed, error info are presented in a dict

        print("change failed")
        if "inconsistent_password" in res :
            return render_user_change(Request, ChangeFailed=True, Inconsistency=True)
        elif "conflict_username" in res :
            return render_user_change(Request, ChangeFailed=True, UsedName=True)
        else :
            raise NotImplementedError("Error not handled in views.change")
    
    return render_user(Request)