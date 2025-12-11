from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django_ratelimit.decorators import ratelimit  # type: ignore

from diagramapp.diagramGenerator.main import generate_diagram
from diagramapp.diagramGenerator.inputValidation import is_valid_input

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def index(request):
    template = loader.get_template('index.html')
    context = {
        # Example context; you can add whatever your page needs
        'copyDisabled': True,
    }
    return HttpResponse(template.render(context, request))

@ratelimit(key='ip', rate='10/m')
def generate(request):
    sentence = request.body.decode('utf-8')

    validation_response = is_valid_input(sentence, request.headers.get('max-diagram-width'))
    if not validation_response.valid:
        return JsonResponse({"ok": False, "reasons": validation_response.reasons})
    
    max_width = int(request.headers.get('max-diagram-width'))
    generator_response = generate_diagram(sentence, max_width)
    
    return JsonResponse({
        "ok" : generator_response.ok,
        "output" : generator_response.output,
        "reasons" : generator_response.reasons
    })
