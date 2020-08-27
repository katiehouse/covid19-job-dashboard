from django.urls import path
from django.urls import re_path, include
from . import views

urlpatterns = [
    path('', views.jobs, name='jobs'),
    re_path(r'^celery-progress/', include('celery_progress.urls')),  
]