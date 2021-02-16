from .models import *
from moss.models import *

def definer_func(taxon_name, from_tax, to_tax, additional_tax=None):
	taxon = Subclass.objects.get(name=taxon_name)
	taxon_bounds = Order.objects.select_related().filter(parent_taxon=taxon.id)
	images = FamilyImages.objects.all()
	order_bounds = [Family.objects.select_related().filter(parent_taxon=order) for order in taxon_bounds]
	card = None

	card_obj = TaxonSearch.objects.get(activation='Act')
	#добавление названия таксона в карточку, на который до этого нажал пользователь
	if card_obj:
		form = SearchCreation(request.POST, instance=card_obj)
		if form.is_valid():
			form = form.save(commit=False)
			form.subclass = str(taxon)
			form.save()

	#определение внутри функции сущестования объекта вместо определения в файле html
	if card_obj != None:
		card = card_obj


class DefinerHandling(taxon_name):
	self.taxon_name = taxon_name
	self.taxons_list = [Class, Subclass, Order, Family, Genus, Species]
	self.images_list = [ClassImages, SubclassImages, OrderImages, FamilyImages, GenusImages, SpeciesImages]

	def taxon_finding(self):
		for tax in taxons_list:
			try:
				taxon = tax.objects.get(name=self.taxon_name)
				return taxon
			except:
				pass

	def class_name(self):
		pass

	def taxon_bounds(self):
		for tax in taxons_list:
			try:
				taxon = tax.objects.get(name=self.taxon_name)
				for tax in taxons_list:
					try:
						tax.objects.select_related.filter(parent_taxon.name=taxon_name):
						return tax
					except:
						pass

			except:
				pass


