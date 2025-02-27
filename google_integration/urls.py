"""
URL configuration for google_integration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from .views import google_login, google_callback,upload_to_drive,list_drive_files
urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", google_login),
    path("auth/callback/", google_callback),
    path("drive/upload/", upload_to_drive),
    path("drive/list/", list_drive_files),
]

