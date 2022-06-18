from django.shortcuts import render

def render_user(request) :
    context          = {}
    return render(request, 'user.html', context)