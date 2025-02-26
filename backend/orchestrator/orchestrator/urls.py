from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), 
    path('downloader/', include('downloader.urls')),  
    path('transcriber/', include('transcriber.urls')), 
    path('summarization/', include('summarization.urls')),  
    # path('report/', include('report.urls')),  
    # path('rag/', include('rag.urls')),  
]
