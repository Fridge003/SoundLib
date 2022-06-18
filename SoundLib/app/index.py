from django.shortcuts import render

def render_index(original_request) :
    context          = {}
    context['hello'] = 'PKUpiano Sound Library!'
    return render(original_request, 'index.html', context)