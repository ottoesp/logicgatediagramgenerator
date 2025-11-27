from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from diagramapp.diagramGenerator.main import generate_diagram

def index(request):
    template = loader.get_template('index.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry'],
        'copyDisabled': True,
    }
    return HttpResponse(template.render(context, request))

def generate(request):
    return JsonResponse({"output": generate_diagram("(A and B) or (C and D) or E", 6)})
# Create your views here.
