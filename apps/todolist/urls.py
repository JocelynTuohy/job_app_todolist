"""
To-Do List urls
---
Jocelyn Tuohy
iTrellis application 2017
"""

from django.conf.urls import url
from . import views

app_name = 'todolist'

urlpatterns = [
    url(r'^overview$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^(?P<todo>\d+)$', views.more, name='more'),
    url(r'^delete/(?P<todo>\d+)$', views.delete, name='delete'),
    url(r'^complete/(?P<todo>\d+)$', views.complete, name='complete'),
]
