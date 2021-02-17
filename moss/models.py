from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from definer.models import *

'''Каждый класс определяет объекты на разных иерархических ступенях систематики растений'''
class Division(models.Model):
	parent_taxon = models.CharField(max_length=50, default='Plantae')
	name = models.CharField(max_length=60)
	description = models.TextField(blank=True)
	definer_description = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	tax = models.ForeignKey(Taxa, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Divisions'


class Class(models.Model):
	parent_taxon = models.ForeignKey(Division, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=60)
	description = models.TextField(blank=True)
	definer_description = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	tax = models.ForeignKey(Taxa, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Classes'

class Subclass(models.Model):
	parent_taxon = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=60)
	description = models.TextField(blank=True)
	definer_description = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	tax = models.ForeignKey(Taxa, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Subclasses'

class Order(models.Model):
	parent_taxon = models.ForeignKey(Subclass, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=60)
	description = models.TextField(blank=True)
	definer_description = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	tax = models.ForeignKey(Taxa, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Orders'


class Family(models.Model):
	parent_taxon = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=60)
	description = models.TextField(blank=True)
	definer_description = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	tax = models.ForeignKey(Taxa, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Families'


class Genus(models.Model):
	parent_taxon = models.ForeignKey(Family, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=60)
	description = models.TextField(blank=True, null=True)
	definer_description = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	tax = models.ForeignKey(Taxa, on_delete=models.SET_NULL, blank=True, null=True)


	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Genuses'

class Species(models.Model):
	parent_taxon = models.ForeignKey(Genus, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=60)
	description = models.TextField(blank=True)
	definer_description = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	tax = models.ForeignKey(Taxa, on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Species'

	def get_absolute_file_upload_url(self):
		return MEDIA_URL + self.img.url


#Изображения привязанные к каждому объекту из предыдущих классов
class SpeciesImages(models.Model):
	taxon = models.ForeignKey(Species, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='species', null=True)

class GenusImages(models.Model):
	taxon = models.ForeignKey(Genus, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='genus', null=True)

class FamilyImages(models.Model):
	taxon = models.ForeignKey(Family, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='family', null=True)

class OrderImages(models.Model):
	taxon = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='order', null=True)

class SubclassImages(models.Model):
	taxon = models.ForeignKey(Subclass, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='subclass', null=True)

class ClassImages(models.Model):
	taxon = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='class', null=True)

class DivisionImages(models.Model):
	taxon = models.ForeignKey(Division, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='division', null=True)

class TaxonOnMap(models.Model):
	'''Точка на карте'''
	relation = models.ForeignKey(Species, on_delete=models.SET_NULL, blank=True, null=True)
	name = models.CharField(max_length=100)
	lat = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
	lon = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
	image = models.ImageField(upload_to='map_images', blank=True, null=True)
	comment = models.TextField(blank=True, null=True)
	creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)


class Profile(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	username = models.CharField(max_length=60, null=True, blank=True)
	name = models.CharField(max_length=60)
	email = models.CharField(max_length=50, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True, null=True)
	picture = models.ImageField(null=True, blank=True) 

	def __str__(self):
		return str(self.username)

#Книги, чебные материалы
class Book(models.Model):
	title = models.CharField(max_length=100)
	file = models.FileField(upload_to='books')
	counter = models.PositiveIntegerField(default=0, verbose_name='Количество скачиваний')

	def __str__(self):
		return str(self.title)

class HomepageImages(models.Model):
	'''Класс для хранения данных о случайным образом отобранных таксонах с изображениями 
	для вывода на домашней странице'''
	img_field = models.TextField(blank=True)