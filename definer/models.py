from django.db import models
from moss.models import *

class Taxa(models.Model):
	'''Название таксона на русском и английском, для дальнейшего использовани этой информации'''
	name = models.CharField(max_length=150) #на русском
	identifier = models.CharField(max_length=150, null=True) #на английском

	def __str__(self):
		return self.name

class TaxonSearch(models.Model):
	'''Карточки для хранения информации о поиске и отображении её при продвижении по иерархическому дереву таксонов
	во время определения растения'''
	division =  models.CharField(max_length=150, blank=True)
	moss_class = models.CharField(max_length=150, blank=True)
	subclass = models.CharField(max_length=150, blank=True)
	order = models.CharField(max_length=150, blank=True)
	family = models.CharField(max_length=150, blank=True)
	genus = models.CharField(max_length=150, blank=True)
	species = models.CharField(max_length=150, blank=True)

	activation_vars = (
		('Act', 'Act'),
		('Deact', 'Deact'),
		('Frozen', 'Frozen')
		)
	#Определяет текущее состояние карточки. Act - отображается во время поиска и изменяется; Frozen - может продолжать
	#отображаться, но не изменяется; Deact - не  отображается
	activation = models.CharField(max_length=30, choices=activation_vars, default='Act', blank=True)