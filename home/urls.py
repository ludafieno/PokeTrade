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
    path('trade/respond/<int:trade_id>/', views.respond_trade, name='respond_trade'),
    path('logout/', views.logout_view, name='logout'),
    path('report/', views.report_issue, name='report'),
    path('choose_starter/', views.choose_starter, name='choose_starter'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('pokemon/<int:pokemon_id>/', views.pokemon_detail, name='pokemon_detail'),
    path('trade/respond/<int:trade_id>/', views.respond_trade, name='respond_trade'),
    path('pokemon/<int:pokemon_id>/list/',views.create_listing,name='create_listing'),
    path('listing/<int:listing_id>/buy/',views.buy_listing,name='buy_listing'),
    path('pending-trades/', views.pending_trades, name='pending_trades'),
    path('pending-trades/<int:trade_id>/respond/', views.respond_trade, name='respond_trade'),
]