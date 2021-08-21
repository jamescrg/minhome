from django.urls import path
from . import views
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

urlpatterns = [
    path('', views.index, name='contacts')
]
