from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import *
from .models import Offre

# Create your views here.


class Offre_list(ListView):
    model = Offre
    template_name = 'offre/list.html'
    context_object_name = 'offres'


class Offre_Details(DetailView):
    model = Offre
    template_name = 'offre/details.html'
    context_object_name = 'offre'


class Offre_Create(CreateView):
    model = Offre
    template_name = 'offre/form.html'
    success_url = reverse_lazy('offre_list')

    form_class = OffreForm


class Offre_Update(UpdateView):
    model = Offre
    template_name = 'offre/update.html'
    success_url = reverse_lazy('offre_list')
    form_class = OffreForm


class Offre_Delete(DeleteView):
    model = Offre
    template_name = 'offre/confirm_delete.html'
    success_url = reverse_lazy('offre_list')
