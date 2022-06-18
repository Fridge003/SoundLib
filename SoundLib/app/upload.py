from django import forms
from django.core.files.storage import FileSystemStorage

def process_upload(file, meta) :

    fs = FileSystemStorage(location="Uploaded")
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)

    return uploaded_file_url