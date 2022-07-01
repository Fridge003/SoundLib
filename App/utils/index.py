from tabnanny import verbose
from django.shortcuts import render
from App.models import User, Recording
from django.conf import settings
from django.db.models import Count

def render_index(OriginalRequest, SelectedTag=None) :

    if SelectedTag is None :
        SelectedTag = "TimeLine"

    UserList = User.objects.annotate(NumRecordings=Count('Recordings'))
    RecordingList = Recording.objects.order_by('-UploadTime')

    context                 = {}
    context['hello']        = 'PKUpiano Sound Library!'
    context['UserList']     = UserList[:settings.ITEMS_PER_PAGE]
    context['RecordingList']= RecordingList[:settings.ITEMS_PER_PAGE]
    context['SelectedTag']  = SelectedTag

    for item in context['UserList'] :
        item.view(verbose=False)
    
    # context['user_authenticated'] = original_request.user.is_authenticated
    return render(OriginalRequest, 'index.html', context)