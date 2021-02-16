from django.contrib import admin
from .models import *

models_list = [Species, Genus, Family, Order, Subclass, Class, Division, SpeciesImages, GenusImages, DivisionImages,
 SubclassImages, Profile, Book, HomepageImages, TaxonOnMap]
for i in models_list:
	admin.site.register(i)
