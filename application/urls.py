"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.index, name="homepage"),

    ### login api #### if needed for getting token ######
    path('user/login/', views.obtain_token, name='api-tokn'),

    ### register api #####
    path('user/register/',views.register,name='register'),

    ## Advisor post
    path('adminn/advisor/', views.AdvisorPostList, name='Add-Advisor'),
    ## Get Advisor
    path('user/<user>/advisor', views.AdvisorGetList, name='Get-Advisor'),

    ## book a call
    path('user/<user>/advisor/<Advisor_id>/', views.BookacallList, name='book_a_call'),
    path('user/<user>/advisor/booking', views.callGetList, name='Get-booked_call'),
]
