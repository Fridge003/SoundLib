from django.shortcuts import render
from django import forms
from django.core.files.storage import FileSystemStorage

import datetime

from SoundLib.app.index import render_index
from SoundLib.app.upload import process_upload

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
 
def hello(request):
    
    return render_index(request)

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