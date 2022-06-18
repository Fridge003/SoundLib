from django.shortcuts import render

def render_index(original_request) :
    context          = {}
    context['hello'] = 'PKUpiano Sound Library!'
    # context['user_authenticated'] = original_request.user.is_authenticated
    return render(original_request, 'index.html', context)