from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import AntiSpf

from django.http import JsonResponse
# Create your views here.

class AntiSpfView(ListView):
    queryset = AntiSpf.objects.filter()
    template_name = 'antispf/antispf.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context