from django.shortcuts import render
from .models import *
# from django.http import HttpResponse
# Create your views here.


def home(request):
    context={
        'posts':Post.objects.all()
    }
    return render(request, 'blogapp/home.html',context)

def about(request):
    return render(request, 'blogapp/about.html')