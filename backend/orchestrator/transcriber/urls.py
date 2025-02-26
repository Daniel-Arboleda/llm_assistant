from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.transcriber_status, name='transcriber_status'), 
    path('manual/', views.manual_transcribe, name='manual_transcribe'),
    path('process_audio/', views.process_downloaded_audio, name='process_downloaded_audio')
]
