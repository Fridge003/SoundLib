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
from App.utils.user import render_user, process_change_form

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
 
def hello(Request):
    
    return render_index(Request)

@login_required
def upload(Request):
    RecordingName = Request.POST['RecordingName']
    ComposerName = Request.POST['ComposerName']
    Description = Request.POST['Description']
    UploadTime = datetime.datetime.now()
    MyFile = Request.FILES['File']
    if Request.method == 'POST' and MyFile:

        save_url = process_upload(MyFile, {
            "RecordingName": RecordingName,
            "ComposerName": ComposerName,
            "Description": Description,
            "UploadTime": UploadTime
        })

        print("file {0} saved as {1}".format(MyFile.name, save_url))

        return render_index(Request)
    return render_index(Request)

def login(Request):

    if Request.user.is_authenticated:

        return render_user(Request)

    return render_login(Request)

def login_form(Request):

    UserName = Request.POST['UserName']
    Password = Request.POST['Password']

    res = process_login_form(Request, UserName, Password)

    if res == True :    # success
        return redirect('/')
    else : # failure
        return render_login(Request, login_failed=True)

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

def logout(Request) :

    logout_user(Request)

    return render_index(Request)

def change_user_info(Request) :

    print(Request.user.get_introduction())

    UserName = Request.POST['UserName']
    Email = Request.POST['Email']
    Password = Request.POST['Password']
    Password2 = Request.POST['Password2']
    Introduction = Request.POST['Introduction']

    res = process_change_form(Request, UserName, Email, Password, Password2, Introduction)

    if res == True :

        print("changed successfully, refreshing...")
        logout_user(Request)
        res = process_login_form(Request, UserName, Password)
        if res == True :    # success
            return render_user(Request)
        else : # failure
            return render_login(Request, login_failed=True)

    else :

        print("change failed")
        if "inconsistent_password" in res :
            return render_user(Request, ChangeFailed=True, Inconsistency=True)
        elif "conflict_username" in res :
            return render_user(Request, ChangeFailed=True, UsedName=True)
        else :
            raise NotImplementedError("Error not handled in views.change")

    return render_user(Request)