from tabnanny import verbose
from django.shortcuts import render
from App.models import User
from django.conf import settings
from django.db.models import Count

def render_index(original_request) :

    UserList = User.objects.annotate(NumRecordings=Count('Recordings'))

    context          = {}
    context['hello'] = 'PKUpiano Sound Library!'
    context['UserList'] = UserList[:settings.ITEMS_PER_PAGE]

    for item in context['UserList'] :
        item.view(verbose=False)
    
    # context['user_authenticated'] = original_request.user.is_authenticated
    return render(original_request, 'index.html', context)