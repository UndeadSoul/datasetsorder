"""
URL configuration for datasetsorder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import HttpResponse
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    
    path('upload/',views.upload_file, name='upload_file'),
    path('success/',views.success, name='success'),
    path('clean_data/',views.clean_data, name='clean_data'),

    path('upload_file_date/',views.upload_file_date, name='upload_file_date'),
    path('success_date/',views.success_date, name='success_date'),
    path('clean_data_date/',views.clean_data_date, name='clean_data_date'),
    
    path('upload_file_places/', views.upload_file_places, name='upload_file_places'),
    path('success_places/', views.success_places, name='success_places'),
    path('clean_data_address/', views.clean_data_address, name='clean_data_address'),

    path('download_records/', views.export_csv, name='download_records'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)