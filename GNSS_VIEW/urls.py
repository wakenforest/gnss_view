"""GNSS_VIEW URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.views import static

from main.views import IndexView, com_data, com_pos, com_antispf
from com.views import ComView, echarts_data
from datashow.views import DataShowView
from antispf.views import AntiSpfView

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', IndexView.as_view(), name = 'index'),
    path('com/', ComView.as_view(template_name = 'com/com.html'), name='random-url'),
    path('datashow/', DataShowView.as_view(template_name = 'datashow/datashow.html'), name='recv-data-url'),
    path('antispf/', DataShowView.as_view(template_name = 'antispf/antispf.html'), name='antispf-url'),


    path('api/echarts/', echarts_data, name='api-echarts'),
    path('api/com_pos/', com_pos, name='api-com-pos'),
    path('api/com_antispf/', com_antispf, name='api-com-antispf'),

    path('api/com_data/', com_data, name='api-com-data'),

    url(r'^static/(?P<path>.*)$', static.serve,
    {'document_root': settings.STATIC_ROOT}, name='static'),
]
