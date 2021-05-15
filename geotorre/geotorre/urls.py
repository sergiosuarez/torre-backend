"""geotorre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.models import User
from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("get_allUsernames", views.get_allUsernames, name="get_allUsernames"),
    path("get_location_user", views.get_location_username, name="get_location_username"),
    path("get_allmembers_xopportunity", views.get_allmembers_xopportunity, name="get_allmembers_xopportunity"),
    path("get_request_opportxskill", views.get_request_opportxskill, name="get_request_opportxskill"),
    path("get_request_peoplexskill", views.get_request_peoplexskill, name="get_request_peoplexskill"),
    
]
