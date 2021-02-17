from django.contrib import admin
from django.urls import path
from . import views

app_name = 'definer'

urlpatterns = [
	path('definer_starter/', views.definer_starter, name='definer_starter'),	 #name - чтобы вызывать 
    path('unitaxon/<str:taxon_name>/', views.definer_unitaxon, name='definer_unitaxon'),   #функцию через html
    path('definer_subclass/<int:card_id>/', views.activation, name='activation'),
    path('cards_list/<int:card_id>/', views.activation_in_cards_list, name='activation_in_cards_list'),
    path('activation/<str:taxon_name>/<int:card_id>/', views.activation_in_unitaxon, name='activation_in_unitaxon'),
    path('freezing/<str:taxon_name>/<int:card_id>/', views.card_freezing, name='card_freezing'),
    path('card_freezing_starter/<int:card_id>/', views.card_freezing_starter, name='card_freezing_starter'),
    path('delete_card/<int:card_id>/', views.delete_card, name='delete_card'),
    path('taxons_observation/<str:taxon_name>/<int:card_id>/', views.taxons_observation, name='taxons_observation'),
    path('cards_list/', views.cards_list, name='cards_list'),
    path('cards_list_freezing/<int:card_id>/', views.cards_list_freezing, name='cards_list_freezing'),

]