from math import ceil
from tabnanny import verbose
from django.shortcuts import render
from App.models import User, Recording
from django.conf import settings
from django.db.models import Count

def render_index(OriginalRequest, SelectedTag=None, SelectedPage=None) :

    HavePages = True

    if SelectedTag is None :
        SelectedTag = "timeline"
    
    if SelectedPage is None :
        SelectedPage = 0
        HavePages = False

    UserList = User.objects.annotate(NumRecordings=Count('Recordings'))
    RecordingList = Recording.objects.order_by('-UploadTime')


    if SelectedTag == "timeline" :
        PageNum = ceil(len(RecordingList)/settings.ITEMS_PER_PAGE)
    elif SelectedTag == "members" :
        PageNum = ceil(len(UserList)/settings.ITEMS_PER_PAGE)
    else :
        PageNum = 0
    
    context                 = {}
    context['RecordingList']= RecordingList[SelectedPage*settings.ITEMS_PER_PAGE : (SelectedPage+1)*settings.ITEMS_PER_PAGE]
    context['UserList']     = UserList[SelectedPage*settings.ITEMS_PER_PAGE: (SelectedPage+1)*settings.ITEMS_PER_PAGE]
    context['hello']        = 'PKUpiano Sound Library!'
    context['SelectedTag']  = SelectedTag
    context['CurrentPage']  = SelectedPage
    context['HavePages']    = HavePages
    context['PageRange']    = list(range(max(0, SelectedPage-2), min(PageNum, SelectedPage+3)))
    context['PagePrefix']   = '/index/'+SelectedTag+'/'
    context['PrevPage']     = max(0, SelectedPage-1)
    context['NextPage']     = min(PageNum-1, SelectedPage+1)

    for item in context['UserList'] :
        item.view(verbose=False)
    
    # context['user_authenticated'] = original_request.user.is_authenticated
    return render(OriginalRequest, 'index.html', context)