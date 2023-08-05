from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='blog-home'),
    path('about/', about, name='blog-about'),
]