"""lesson_27 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from ads import views
from ads.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('ad/', AdsViews.as_view()),
    path('cat/', CatViews.as_view()),
    path('ad/<int:pk>', AdsViewId.as_view()),
    path('cat/<int:pk>', CatViewId.as_view()),
]
