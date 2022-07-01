from django.shortcuts import render
from django.db.utils import IntegrityError
from App.models import Recording

def render_recording_info(Request, Recordings) :
    Context                  = {}
    Context["RecordingList"] = Recordings
    return render(Request, 'recording.html', Context)

def render_recording_change(Request, Recordings) :

    Context                  = {}
    Context["RecordingList"] = Recordings
    return render(Request, 'recording_change.html', Context)