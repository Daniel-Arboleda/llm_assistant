from django.urls import path
from .views import process_transcript

urlpatterns = [
    path('process_transcript/', process_transcript, name='process_transcript'),
]
