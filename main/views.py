from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Index
from .com_recv import COM_RECV
from django.http import JsonResponse

import json
import serial
import threading
import time
import re
import random
from collections import deque

# Create your views here.

update_jsondata={}

def gen_antispf_stream(jsondata,row_idx,dq_data,DATA_SHOW_LEN):
    tmp_power = (int)(jsondata[row_idx][3])
    if len(dq_data[row_idx])<DATA_SHOW_LEN:
        dq_data[row_idx].append(tmp_power)
    else:
        dq_data[row_idx].pop(0)
        dq_data[row_idx].append(tmp_power)

def jieshou(x):

    global update_jsondata
    global dq_height, dq_time, dq_pos, MAX_SATNUM,DATA_SHOW_LEN
    global dq_power, dq_satList, dq_cn0, dq_sqm1, dq_sqm2, dq_dopchk

    DATA_SHOW_LEN = 50
    MAX_SATNUM = 24

    dq_height = []
    dq_time = []
    dq_pos = []

    dq_power = [[0 for i in range(MAX_SATNUM)] for j in range(DATA_SHOW_LEN)]
    dq_cn0 = [[0 for i in range(MAX_SATNUM)] for j in range(DATA_SHOW_LEN)]
    dq_sqm1 = [[0 for i in range(MAX_SATNUM)] for j in range(DATA_SHOW_LEN)]
    dq_sqm2 = [[0 for i in range(MAX_SATNUM)] for j in range(DATA_SHOW_LEN)]
    dq_dopchk = [[0 for i in range(MAX_SATNUM)] for j in range(DATA_SHOW_LEN)]
    dq_satList = [0 for i in range(MAX_SATNUM)]

    data = ""
    jsondata = {}
    end_flag = "end"
    row_idx = 0

    while True:
        while x.inWaiting() > 0:
            data = x.readline().decode()
            if 'pos' in data:
                pattern = re.compile(r"pos:(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)\n")
                match = pattern.match(data)
                if match:
                    print(match.groups())
                    print(row_idx)
                    jsondata[row_idx] = list( match.groups() )
                    row_idx = row_idx + 1

                    # deal with lat list
                    tmp_pos = [ match.groups()[0], match.groups()[1] ]
                    if len(dq_pos)<DATA_SHOW_LEN:
                        dq_pos.append(tmp_pos)
                    else:
                        dq_pos.pop(0)
                        dq_pos.append(tmp_pos)

                    # deal with height list
                    tmp_h = match.groups()[2]
                    if len(dq_height)<DATA_SHOW_LEN:
                        dq_height.append(tmp_h)
                    else:
                        dq_height.pop(0)
                        dq_height.append(tmp_h)

                    # deal with time list
                    tmp_t = match.groups()[3]
                    if len(dq_time)<DATA_SHOW_LEN:
                        dq_time.append(tmp_t)
                    else:
                        dq_time.pop(0)
                        dq_time.append(tmp_t)
                    
            else:
                pattern = re.compile(r"(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)\r\n")
                match = pattern.match(data)
                if match:
                    # print(match.groups())
                    jsondata[row_idx] = list( match.groups() )
                    jsondata[row_idx][4] = (float)(jsondata[row_idx][4])
                    
                    dq_satList[row_idx] = (int)(jsondata[row_idx][1])

                    # deal with power
                    # gen_antispf_stream(jsondata,row_idx,dq_power,DATA_SHOW_LEN)
                    tmp_power = (int)(jsondata[row_idx][3])
                    if len(dq_power[row_idx])<DATA_SHOW_LEN:
                        dq_power[row_idx].append(tmp_power)
                    else:
                        dq_power[row_idx].pop(0)
                        dq_power[row_idx].append(tmp_power)
                    
                    # deal with cn0
                    tmp_cn0 = (float)(jsondata[row_idx][4])
                    if len(dq_cn0[row_idx])<DATA_SHOW_LEN:
                        dq_cn0[row_idx].append(tmp_cn0)
                    else:
                        dq_cn0[row_idx].pop(0)
                        dq_cn0[row_idx].append(tmp_cn0)

                    # # deal with sqm_r
                    # tmp_cn0 = (float)(jsondata[row_idx][4])
                    # if len(dq_cn0[row_idx])<DATA_SHOW_LEN:
                    #     dq_cn0[row_idx].append(tmp_cn0)
                    # else:
                    #     dq_cn0[row_idx].pop(0)
                    #     dq_cn0[row_idx].append(tmp_cn0)
                    
                    row_idx = row_idx + 1
                
        # 完整接收了一帧串口数据
        if end_flag in data:
            # print(jsondata)
            update_jsondata = jsondata
            data = ""
            jsondata = {}
            row_idx = 0

# table data transfer
def com_data(request):
    global update_jsondata
    return JsonResponse(update_jsondata)


# table data transfer
def com_pos(request):
    global dq_height,dq_time,dq_pos
    len_pos = len(dq_height)
    x = list( range(0,len_pos) ) 
    
    pos_jsondata = {
        "key": x,
        "pos": dq_pos,
        "height": dq_height,
        "time":dq_time,
    }
    return JsonResponse(pos_jsondata)

# antispf
def com_antispf(request):
    global dq_power,dq_satList, DATA_SHOW_LEN,dq_cn0
    len_power = DATA_SHOW_LEN
    x = list( range(0,len_power) ) 
    
    antispf_jsondata = {
        "key": x,
        "satList": dq_satList,
        "power": dq_power,
        "cn0":dq_cn0,
    }
    return JsonResponse(antispf_jsondata)


class IndexView(ListView):
    queryset = Index.objects.filter()
    template_name = 'main/index.html'
    context_object_name = 'data'
    com_open_success = True

    # global x

    try:
        x = serial.Serial('COM3',115200)
        com_open_success = True
    except:
        com_open_success = False

    if(com_open_success):
        t1 = threading.Thread(target=jieshou,args=(x,),name="jieshou")
        t1.start()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
