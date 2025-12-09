"""
URL configuration for qualityEducation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('campusConnect.urls')),

    # Django built-in authentication URLs (login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
]
