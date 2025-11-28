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
    wff = request.body.decode('utf-8')
    try:
        output = generate_diagram(wff, 8)
    except Exception as e:
        output = str(e)
    return JsonResponse({"output": output})
# Create your views here.
