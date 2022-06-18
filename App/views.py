from django.shortcuts import render
from django import forms
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user

import datetime

from App.utils.index import render_index
from App.utils.login import render_login, process_login_form, process_register_form
from App.utils.upload import process_upload
from App.utils.user import render_user

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
 
def hello(request):
    
    return render_index(request)

@login_required
def upload(request):
    RecordingName = request.POST['RecordingName']
    ComposerName = request.POST['ComposerName']
    Description = request.POST['Description']
    UploadTime = datetime.datetime.now()
    MyFile = request.FILES['File']
    if request.method == 'POST' and MyFile:

        save_url = process_upload(MyFile, {
            "RecordingName": RecordingName,
            "ComposerName": ComposerName,
            "Description": Description,
            "UploadTime": UploadTime
        })

        print("file {0} saved as {1}".format(MyFile.name, save_url))

        return render_index(request)
    return render_index(request)

def login(request):

    if request.user.is_authenticated:

        return render_user(request)

    return render_login(request)

def login_form(request):

    UserName = request.POST['UserName']
    Password = request.POST['Password']

    return process_login_form(request, UserName, Password)

def register_form(request):

    UserName = request.POST['UserName']
    Email = request.POST['Email']
    Password = request.POST['Password']
    Password2 = request.POST['Password2']

    return process_register_form(request, UserName, Email, Password, Password2)

def logout(request) :

    logout_user(request)

    return render_index(request)