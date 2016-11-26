"""ttt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^targets/', views.targets),
    url(r'^getPangSub/', views.getPangSub),
    url(r'^xcdn/', views.xcdn),
    url(r'^highRisk/', views.highRisk),
    url(r'^sqli/', views.sqli),
    url(r'^xdir/', views.xdir),
    url(r'^xcms/', views.xcms),
    url(r'^xwebshell/', views.xwebshell),
    url(r'^xadmin/', views.xadmin),
    url(r'^xwaf/', views.xwaf),
    url(r'^dbquery/', views.dbquery),
    url(r'^result/',views.result),
]
