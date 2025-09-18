from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry'],
        'copyDisabled': True,
    }
    return HttpResponse(template.render(context, request))

def generate(request):

    return JsonResponse({"output": "bar"})
# Create your views here.
