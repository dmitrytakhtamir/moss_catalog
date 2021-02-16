from .models import *


class TaxonFinder(object):
	def __init__(self, name):
		self.name = name 
		self.taxons_list = [Division, Class, Subclass, Order, Family, Genus, Species]
		self.images_list = [DivisionImages, ClassImages, SubclassImages, OrderImages, FamilyImages, GenusImages, SpeciesImages]
		self.list_of_obj = []
	#нахождение объекта
	def taxon_object(self):
		for tax in self.taxons_list:
			try:
				taxon = tax.objects.get(name=self.name)
				return taxon
			except:
				pass

	#модель, к которой относится объект
	def taxon_model(self):
		for tax in self.taxons_list:
			try:
				taxon = tax.objects.get(name=self.name)
				return tax
			except:
				pass

	def taxon_bounds(self):
		for tax in self.taxons_list:
			try:
				taxon = tax.objects.get(name=self.name)
				list_of_obj = []
				for tax in self.taxons_list:
					try:
						class_objects = tax.objects.all()
						
						for obj in class_objects:
							if obj.parent_taxon == taxon:
								list_of_obj.append(obj)
							else:
								pass
					except:
						pass
				return list_of_obj 

			except:
				pass


	#связанные с объектом изображения			
	def taxon_images(self):
		taxon = None
		for tax in self.taxons_list:
			try:
				taxon = tax.objects.get(name=self.name)
			except:
				pass
		for img in self.images_list:
			try:
				image = img.objects.select_related().filter(taxon=taxon)
				return image
			except:
				pass
				
	#модель связанных изображений
	def taxon_images_model(self):
		taxon = None
		for tax in self.taxons_list:
			try:
				taxon = tax.objects.get(name=self.name)
			except:
				pass
		for img in self.images_list:
			try:
				image = img.objects.select_related().filter(taxon=taxon)
				return img
			except:
				pass