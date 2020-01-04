from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import COM

from django.http import JsonResponse
import random

import threading
import time
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

class ComView(ListView):
    queryset = COM.objects.filter()
    template_name = 'com/com.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

dataLen = 50
ylist =  [0 for _ in range(dataLen)]
def thread_func():
    global ylist,dataLen
    n = -4 + random.randint(0, 10)
    ylist[dataLen-1] = ylist[dataLen-1] + n
    for i in range(dataLen-1):
        ylist[i] = ylist[i+1]
    

def echarts_data(request):
    global dataLen
    x = list( range(0,dataLen) ) 
    
    timer = threading.Timer(1, thread_func)
    timer.start()
    
    jsondata = {
        "key": x,
        "value": ylist,
    }
    return JsonResponse(jsondata)