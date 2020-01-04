from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import DataShow

from django.http import JsonResponse
# Create your views here.

class DataShowView(ListView):
    queryset = DataShow.objects.filter()
    template_name = 'datashow/datashow.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context