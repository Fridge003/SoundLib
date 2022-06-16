from django.http import HttpResponse
from django.shortcuts import render
 
def hello(request):
    context          = {}
    context['hello'] = 'PKUpiano Sound Library!'
    return render(request, 'index.html', context)