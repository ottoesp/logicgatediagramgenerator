from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World! We at the index ovah here")

# Create your views here.
