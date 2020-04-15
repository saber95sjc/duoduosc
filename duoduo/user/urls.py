"""duoduo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('detail/', views.detail),
    # path('vip/', views.vip_center),
    # path('rz/', views.certification),
    path('invest/', views.invest_money),
    path('withdraw/', views.withdraw_money),
    path('order/', views.release_order),
    path('loot/', views.loot_order),
    path('index/',views.index),
    path('path_img/',views.path),
    path('single/',views.single),
    path('zfrw/',views.zfrw),
    path('',views.sy)
]
