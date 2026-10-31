from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Expedition

# Create your views here.


def home(request):
    return HttpResponse("<h1>Welcome to ...</h1>")

def welcome(request, name):
    return HttpResponse(f"Hello {{ name }}")

def listExpeditions(request):
    list = Expedition.objects.all()
    return render(request, 'expedition/list.html', {"liste":list})

def detailsExpedition(request, pk):
    expedition = Expedition.objects.get(pk=pk)
    return render(request, 'expedition/details.html', {'exp': expedition})

def delete(request, pk):
    Expedition.objects.delete(pk=pk)
    listExpeditions(request)