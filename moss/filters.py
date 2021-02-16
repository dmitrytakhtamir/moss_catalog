import django_filters
from .models import *
from django_filters import DateFilter

class OrderFilter(django_filters.FilterSet):
	class Meta:
		model = Species
		fields = ['name', 'creator']
		exclude = ['img', 'description', 'date']

def filt_search(obj):
	all_sp = Species.objects.all()
	filtered = []

	for sp in all_sp:
		if sp.name == obj:
			filtered.append(sp)

	return filtered

