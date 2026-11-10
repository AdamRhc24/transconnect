from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView
from .models import Expedition

from django.urls import reverse_lazy

# Create your views here.


def home(request):
    return HttpResponse("<h1>Welcome to ...</h1>")

def welcome(request, name):
    return HttpResponse(f"Hello {name}")

def listExpeditions(request):
    expeditions = Expedition.objects.filter(statut='publiee')
    return render(request, 'expedition/list.html', {'expeditions': expeditions})



def detailsExpedition(request, pk):
    expedition = Expedition.objects.filter(pk=pk).first()
    if expedition is None:
        return expedition_not_found(request, reference=f"#{pk}")
    return render(request, 'expedition/details.html', {'expedition': expedition})


def expedition_not_found(request, reference=None):
    """404 page for expedition detail lookups."""
    return render(request, '404.html', {'reference': reference}, status=404)

def delete(request, pk):
    expedition = get_object_or_404(Expedition, pk=pk)
    expedition.delete()
    messages.success(request, "Expedition supprimee avec succes.")
    return redirect('expedition_list')

    
class Expedition_list(ListView):
    model = Expedition
    template_name = 'expedition/list.html'
    context_object_name = 'expeditions'


class Expedition_Details(DetailView):
    model = Expedition
    template_name = 'expedition/details.html'
    context_object_name = 'expedition'

    def get(self, request, *args, **kwargs):
        expedition = Expedition.objects.filter(pk=kwargs.get('pk')).first()
        if expedition is None:
            return expedition_not_found(request, reference=f"#{kwargs.get('pk')}")
        return render(request, self.template_name, {'expedition': expedition})


class Expedition_Delete(DeleteView):
    model = Expedition
    template_name = 'expedition/confirm_delete.html'
    success_url = reverse_lazy('expedition_list')