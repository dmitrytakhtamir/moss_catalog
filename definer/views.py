from django.shortcuts import render, redirect
from .models import *
from moss.models import *
from .forms import *
from moss.functions import *
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.files.base import ContentFile

def definer_unitaxon(request, taxon_name):
	'''Функция для отображения всех страниц, кроме стартовой, при перемещении по определителю'''
	obj = TaxonFinder(name=taxon_name)
	taxon = obj.taxon_object()  #нахождение объекта среди всех используемых для создания мхов моделей
	taxon_bounds = obj.taxon_bounds() #связи объекта с имеющими его в качестве ForeignKey объектами
	images = obj.taxon_images() #связанные с ним изображения
	#название модели объекта, для использования его при выборе заполняемого в карточке атрибута
	model = obj.taxon_model()
	
	#Извлечение всех изображений относящихся к данному классу для распределения их среди объектов в html
	tax_images = None
	if taxon_bounds:
		bound_obj = TaxonFinder(name=taxon_bounds[0])
		model = obj.taxon_model()
		tax_images_model = bound_obj.taxon_images_model()
		tax_images = tax_images_model.objects.all()

	try:
		#Извлечение названия объекта поиска для отображения в заголовке						  
		tax_name = str(taxon_bounds[0].tax).lower()
		if taxon_bounds[0].tax == None:
			if model.__name__ == 'Species':
				tax_name = 'вид'
			else:
				tax_name = 'ранг не задан'
	except:
		if model.__name__ == 'Species':
				tax_name = 'вид'
		else:
			tax_name = 'ранг не задан'

	card = None #определяется в следующем блоке кода
	act_button = None
	freez_button_name = None
	button_name = 'Заморозить'
	freez_button_name = 'Разморозить'
	freez_act_button = None

	try:
		freezing_card = list(TaxonSearch.objects.filter(activation='Frozen'))[-1:]
		freez_button_name = 'Разморозить'
		freez_act_button = 'Активировать'
	except:
		freezing_card = None
		button_name = 'Заморозить'
	#добавление названия таксона в карточку, на который до этого нажал пользователь
	try:
		card = TaxonSearch.objects.get(activation='Act')
		act_button = 'Убрать карточку'
		if card:
			print(card.division, end='after if ')
			#дальнейшая многословность вызвана стиранием информации в карточке после манипуляций с ней
			division = card.division
			moss_class = card.moss_class
			subclass = card.subclass
			order = card.order
			family = card.family
			genus = card.genus
			species = card.species

			form = SearchCreation(request.POST, instance=card)
			print(card.division)

			if form.is_valid():
				print(form.is_valid())
				print(obj.taxon_model().__name__)
				print(model.__name__)
				print(model)
				print(division, end='after is_valid ')
				form = form.save(commit=False)

				if model.__name__ == 'Division':
					form.division = str(taxon)
				elif model.__name__ == 'Class':
					form.division = division
					form.moss_class = str(taxon)
				elif model.__name__ == 'Subclass':
					form.division = division
					form.moss_class = moss_class
					form.subclass = str(taxon)
				elif model.__name__ == 'Order':
					form.division = division
					form.moss_class = moss_class
					form.subclass = subclass
					form.order = str(taxon)
				elif model.__name__ == 'Family':
					form.division = division
					form.moss_class = moss_class
					form.subclass = subclass
					form.order = order
					form.family = str(taxon)
				elif model.__name__ == 'Genus':
					form.division = division
					form.moss_class = moss_class
					form.subclass = subclass
					form.order = order
					form.family = family
					form.genus = str(taxon)
				elif model.__name__ == 'Species':
					form.division = division
					form.moss_class = moss_class
					form.subclass = subclass
					form.order = order
					form.family = family
					form.genus = genus
					form.species = str(taxon)

				form.save()

	except:
		card == None
		act_button = 'Активировать'
	context = {'taxon': taxon, 'taxon_bounds': taxon_bounds, 'images': images, 'card': card,
	 'model': model, 'tax_name': tax_name, 'freezing_card': freezing_card, 'button_name': button_name, 
	 'act_button': act_button, 'freez_button_name': freez_button_name,'freez_act_button': freez_act_button,
	 'tax_images': tax_images}
	return render(request, 'definer_unitaxon.html', context)

def taxons_observation(request, taxon_name, card_id):
	'''Функция для перемещения по уже отмеченным в карточке таксонам без опасности утратить информацию
	или изменить ее'''
	obj = TaxonFinder(name=taxon_name)
	taxon = obj.taxon_object()  #нахождение объекта среди всех используемых для создания мхов моделей
	taxon_bounds = obj.taxon_bounds() #связи объекта с имеющими его в качестве ForeignKey объектами
	images = obj.taxon_images() #связанные с ним изображения
	model = obj.taxon_model().__name__ #название модели объекта, для использования его при выборе 
							  #заполняемого в карточке атрибута
	try:
		#Извлечение названия объекта поиска для отображения в заголовке						  
		tax_name = str(taxon_bounds.tax).lower()
		if taxon_bounds.tax == None:
			tax_name = 'ранг не задан'
	except:
		tax_name = 'ранг не задан'

	card = TaxonSearch.objects.get(id=card_id)
	if card.activation == 'Act':
		act_button = 'Убрать карточку'
		button_name = 'Заморозить'
	elif card.activation == 'Deact':
		act_button = 'Активировать карточку'
		button_name = 'Заморозить'
	elif card.activation == 'Frozen':
		act_button = 'Активировать карточку'
		button_name = 'Разморозить'

	context = {'taxon': taxon, 'taxon_bounds': taxon_bounds, 'images': images, 
	'card': card, 'model': model, 'tax_name': tax_name, 'button_name': button_name, 'act_button': act_button}
	return render(request, 'definer_unitaxon.html', context)

def definer_starter(request):
	'''Стартовая страница для движения по определителю, естьотсутсвующаяя на других страницах определителя 
	возможность создать новую карту, перейти к списку всех карт'''
	#все изображения связанные с классом, которые затем будут распределены по связям с объектами
	division_images = DivisionImages.objects.all()
	moss_list = Division.objects.all()
	search_cards = []
	all_cards = TaxonSearch.objects.all()
	card = None

	#нахождение активной карты
	try:
		card = TaxonSearch.objects.get(activation='Act')
		search_cards.append(card)
	except:
		pass
	#получение списка замороженных карт, и добавление в список для вывода одной или двух последних карт
	try:	
		froz_list = TaxonSearch.objects.filter(activation='Frozen')
		froz = list(froz_list)
		print(froz[::-1])
		frozen_cards = [search_cards.append(card) for card in froz[::-1] if len(search_cards) < 2]
	except:
		pass
	print(search_cards)
	#создание новой карты
	form = SearchCreation()
	if request.method == 'POST':
		form = SearchCreation(request.POST)
		if form.is_valid():
			#проверка, чтоб исключить вероятность появления двух активных карт
			act_cards = TaxonSearch.objects.filter(activation='Act')
			if act_cards:
				for card_obj in act_cards:
					if not card_obj == card:
						division = card_obj.division
						moss_class = card_obj.moss_class
						subclass = card_obj.subclass
						order = card_obj.order
						family = card_obj.family
						genus = card_obj.genus
						species = card_obj.species
						form2 = SearchCreation(request.POST, instance=card_obj)
						if form2.is_valid():
							form2 = form2.save(commit=False)
							form2.activation = 'Deact'
							form2.division, form2.moss_class, form2.subclass = division, moss_class, subclass
							form2.order, form2.family, form2.genus, form2.species = order, family, genus, species
							form2.save()
			#сохранение нового объекта в первой форме с состоянием по-умолчанию Act
			form.save()
			#последняя активная карта, до создания новой, становится замороженной
			if card:
				division = card.division
				moss_class = card.moss_class
				subclass = card.subclass
				order = card.order
				family = card.family
				genus = card.genus
				species = card.species
				form2 = SearchCreation(request.POST, instance=card)
				if form2.is_valid():
					form2 = form2.save(commit=False)
					form2.activation = 'Frozen'
					form2.division, form2.moss_class, form2.subclass = division, moss_class, subclass
					form2.order, form2.family, form2.genus, form2.species = order, family, genus, species
					form2.save()

					try:
						act_card = TaxonSearch.objects.get(activation='Act')
						search_cards.append(act_card)
						search_cards.append(card)
					except:
						pass
					
			return redirect('definer:definer_starter')			
	#названия кнопок
	freez_button_name = 'Разморозить'
	button_name = 'Заморозить'

	context = {'moss_list': moss_list, 'division_images': division_images, 
				'form': form, 'search_cards': search_cards, 'button_name': button_name,
				 'freez_button_name': freez_button_name}
	return render(request, 'definer_starter.html', context)

class Activation():
	'''Класс для определения многократно используемых в дальнейшем функций'''
	def __init__(self, card_id, taxon_name=None):
		self.card = TaxonSearch.objects.get(id=card_id)
		self.all_cards = TaxonSearch.objects.all()

		self.taxon = TaxonFinder(name=taxon_name).taxon_object()

		self.division = self.card.division
		self.moss_class = self.card.moss_class
		self.subclass = self.card.subclass
		self.order = self.card.order
		self.family = self.card.family
		self.genus = self.card.genus
		self.species = self.card.species

	def act_func(self, form):
		form = form.save(commit=False)
		form.activation = 'Deact'

		form.division, form.moss_class, form.subclass = self.division, self.moss_class, self.subclass 
		form.order, form.family, form.genus, form.species = self.order, self.family, self.genus, self.species

		form.save()

	def deact_func(self, form, request):
		form = form.save(commit=False)
		form.activation = 'Act'

		form.division, form.moss_class, form.subclass = self.division,  self.moss_class, self.subclass
		form.order, form.family, form.genus, form.species = self.order, self.family, self.genus, self.species

		form.save()

		for card_obj in self.all_cards:
			if card_obj.id != self.card.id and card_obj.activation == 'Act':
				division = card_obj.division
				moss_class = card_obj.moss_class
				subclass = card_obj.subclass
				order = card_obj.order
				family = card_obj.family
				genus = card_obj.genus
				species = card_obj.species
				form2 = SearchCreation(request.POST, instance=card_obj)
				if form2.is_valid():
					form2 = form2.save(commit=False)
					form2.activation = 'Deact'
					form2.division, form2.moss_class, form2.subclass,= division, moss_class, subclass
					form2.order, form2.family, form2.genus, form2.species = order, family, genus, species
					form2.save()

	def freezing_func(self, form):
		form = form.save(commit=False)
		form.activation = 'Frozen'

		form.division, form.moss_class, form.subclass = self.division,  self.moss_class, self.subclass
		form.order, form.family, form.genus, form.species = self.order, self.family, self.genus, self.species

		form.save()

def activation(request, card_id):
	'''Активация карты на стартовой странице'''
	card_obj = Activation(card_id)
	card = card_obj.card
	form = SearchCreation(instance=card)
	if request.method == 'POST':
		form = SearchCreation(request.POST, instance=card)
		if form.is_valid():
			if card.activation == 'Act':
				card_obj.act_func(form) #деактивирует карту
				return redirect('definer:definer_starter')
			elif card.activation == 'Deact' or card.activation == None or card.activation == 'Frozen':
				card_obj.deact_func(form, request) #активирует
				return redirect('definer:definer_starter')

	return render(request, 'definer_starter.html')

def activation_in_cards_list(request, card_id):
	'''Активация карты в разделе списка всех карт'''
	card_obj = Activation(card_id)
	card = card_obj.card
	form = SearchCreation(instance=card)
	if request.method == 'POST':
		form = SearchCreation(request.POST, instance=card)
		if form.is_valid():
			if card.activation == 'Act':
				card_obj.act_func(form)
				return redirect('definer:cards_list')
			elif card.activation == 'Deact'  or card.activation == None  or card.activation == 'Frozen':
				card_obj.deact_func(form, request)
				return redirect('definer:cards_list')

	return render(request, 'cards_list.html')

def activation_in_unitaxon(request, taxon_name, card_id,):
	'''Активация карты на всех страницах, кроме стартовой'''
	card_obj = Activation(card_id, taxon_name=taxon_name)
	card = card_obj.card
	form = SearchCreation(instance=card)
	if request.method == 'POST':
		form = SearchCreation(request.POST, instance=card)
		if form.is_valid():
			if card.activation == 'Act':
				card_obj.act_func(form)
				return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(card_obj.taxon.name,)))
			elif card.activation == 'Deact'  or card.activation == None  or card.activation == 'Frozen':
				card_obj.deact_func(form, request)
				return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(card_obj.taxon.name,)))

	return render(request, 'definer_unitaxon.html')

def card_freezing_starter(request, card_id):
	'''Заморозка карты на стартовой странице'''
	card_obj = Activation(card_id)
	card = card_obj.card
	form = SearchCreation(instance=card)
	if request.method == 'POST':
		form = SearchCreation(request.POST, instance=card)
		if form.is_valid():
			if card.activation == 'Act' or card.activation == 'Deact':
				card_obj.freezing_func(form)
				return redirect('definer:definer_starter')
			elif card.activation == 'Frozen':
				card_obj.deact_func(form, request)
				return redirect('definer:definer_starter')

	return render(request, 'definer_starter.html')

def card_freezing(request, taxon_name, card_id):
	'''Заморозка карты на всех страницах, кроме стартовой'''
	card_obj = Activation(card_id, taxon_name=taxon_name)
	card = card_obj.card
	form = SearchCreation(instance=card)
	if request.method == 'POST':
		form = SearchCreation(request.POST, instance=card)
		if form.is_valid():
			if card.activation == 'Act' or card.activation == 'Deact':
				card_obj.freezing_func(form)
				return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(card_obj.taxon.name,)))
			elif card.activation == 'Frozen':
				card_obj.deact_func(form, request)
				return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(card_obj.taxon.name,)))
	return render(request, 'definer_unitaxon.html')

def cards_list_freezing(request, card_id):
	'''Заморозка карты на странице списка всех карт'''
	card_obj = Activation(card_id)
	card = card_obj.card
	form = SearchCreation(instance=card)
	if request.method == 'POST':
		form = SearchCreation(request.POST, instance=card)
		if form.is_valid():
			if card.activation == 'Act' or card.activation == 'Deact':
				card_obj.freezing_func(form)
				return redirect('definer:cards_list')
			elif card.activation == 'Frozen':
				card_obj.deact_func(form, request)
				return redirect('definer:cards_list')
	return render(request, 'cards_list.html')

def delete_card(request, card_id):
	'''Удаление карты'''
	card = TaxonSearch(id=card_id)
	if request.method == 'POST':
		card.delete()
		return redirect('definer:cards_list')
	return render(request, 'delete_card.html')

def cards_list(request):
	'''Список всех карт'''
	cards = []

	cards_act = [cards.append(card) for card in TaxonSearch.objects.filter(activation='Act')]
	cards_frozen = [cards.append(card) for card in TaxonSearch.objects.filter(activation='Frozen')]
	cards_deact = [cards.append(card) for card in TaxonSearch.objects.filter(activation='Deact')]
	button_name = 'Заморозить'
	freez_button_name = 'Разморозить'

	return render(request, 'cards_list.html', {'cards': cards, 'button_name': button_name, 
		'freez_button_name': freez_button_name})