from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('collection/', views.collection, name='collection'),
    path('trade/', views.trade, name='trade'),
    path('logout/', views.logout_view, name='logout'),
    path('report/', views.report_issue, name='report'),





]