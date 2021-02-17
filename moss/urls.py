from django.contrib import admin
from django.urls import path
from . import views

app_name = 'taxons'

urlpatterns = [
	path('species_list/', views.species_list, name='species_list'),
	path('genus_list/', views.genus_list, name='genus_list'),
	path('family_list/', views.family_list, name='family_list'),
	path('order_list/', views.order_list, name='order_list'),
	path('subclass_list/', views.subclass_list, name='subclass_list'),
	path('class_list/', views.class_list, name='class_list'),
	path('division_list/', views.division_list, name='division_list'),
	path('multiple_images/<str:taxon_name>/', views.multiple_images, name='multiple_images'),
	path('main_image/<str:taxon_name>/', views.main_image, name='main_image'),
	path('delete_taxon/<str:taxon_name>/', views.delete_taxon, name='delete_taxon'),
	path('book_add/', views.book_add, name='book_add'),
    path('book/<int:book_id>/', views.book, name='book'),
    path('books/', views.books, name='books'),
    path('all_taxons/', views.all_taxons, name='all_taxons'),
    path('universal_taxon/<str:name>/', views.universal_taxon, name='universal_taxon'),
    path('edition/<str:name>/', views.edition, name='edition'),
    path('new_taxon/', views.new_taxon, name='new_taxon'),
    path('homepage_images/', views.homepage_images, name='homepage_images'),




]