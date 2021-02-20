from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.forms import ModelForm, Form
from .decoraitors import *
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .filters import OrderFilter, filt_search
from django.db.models import Q
import folium
from folium.plugins import MarkerCluster
from .new_marker import new_marker
from django.core.files.base import ContentFile
from GPSPhoto import gpsphoto
import os
from pathlib import Path
from folium import IFrame
from folium.plugins import FloatImage
from .functions import *
import random
import sys  #потом удалить
import re


def home(request):
	species = Species.objects.order_by('name')
	all_obj = Species.objects.all()
	myFilter = OrderFilter(request.GET, queryset=species)
	species = myFilter.qs
	books = Book.objects.order_by('title')
	#количество экземпляров разных моделей для вывода их количества на выпадающей панели навбара
	sp_span = len(Species.objects.all())
	gen_span = len(Genus.objects.all())
	fam_span = len(Family.objects.all())
	order_span = len(Order.objects.all())
	subclass_span = len(Subclass.objects.all())
	division_span = len(Division.objects.all())
	books_span = len(Book.objects.all())
	points_span = len(TaxonOnMap.objects.all())
	taxons_list = (Division, Class, Subclass, Order, Family, Genus, Species)
	all_tax_span = 0
	for taxon in taxons_list:
		all_tax_span += len(taxon.objects.all())

	definer = request.GET.get('definer_reverse', '')
	if definer:
		return redirect('definer:definer_first_step') 
	#Удаление ненужных символов из сохраненного в тексте списка 5 случайныхобъектов с изображениями
	new_images = HomepageImages.objects.get(id=1).img_field
	bad_chars = [' \'', '\'', '[', ']']
	for i in bad_chars:
		new_images = new_images.replace(i, '')
	#и преобразование текста в список
	list_of_img_objects =  new_images.split(',')
	images_store = [TaxonFinder(name=i).taxon_object() for i in list_of_img_objects]

	context = {'species': species, 'all_obj': all_obj, 'books': books, 
				'myFilter': myFilter, 'sp_span': sp_span, 'gen_span': gen_span, 'books_span': books_span,
			'points_span': points_span, 'subclass_span': subclass_span, 'images_store': images_store, 
			'fam_span': fam_span, 'order_span': order_span, 'class_span': class_span, 'division_span': division_span,'all_tax_span': all_tax_span}
	return render(request, 'home.html', context)

def homepage_images(request):
	'''Отбирает все объекты имеющие атрибут img (используя в цикле for лямбду в сочетании с filter и map,
	затем выбирает из них случайные 10 экземпляров, и выводит на домашней старнице их изображения'''

	models_list = (Division, Class, Subclass, Order, Family, Genus, Species)
	taxons_with_img =  []
	testt = []
	for model in models_list:
		taxons = model.objects.all()
		tax = list(filter(lambda tax: len(tax.img.name) > 0, model.objects.all()))
		test = list(map(lambda i: taxons_with_img.append(i), tax))

	#отбор случайным образом изображений; их уникальность в коллекции гарантируется свойствами множества
	random_set = set()

	counter = 0
	while True:
		random_tax = random.choice(taxons_with_img)
		random_set.add(random_tax)
		counter += 1
		#цикл завершается либо при заполнении множетсва указанным числом экземпляров,
		#либо при достижении лимита попыток, установленного на случай отсутсвия заданного 
		#количества экземпляров с изображениями
		if len(random_set) >= 6 or counter == 50:
			break

	#сохранение множества в виде str в TextField объекта
	form = HomepageImagesForm(instance=HomepageImages.objects.get(id=1))
	if request.method == 'GET':
		form = HomepageImagesForm(request.GET, instance=HomepageImages.objects.get(id=1))
		if form.is_valid():
			form = form.save(commit=False)
			form.img_field = [i.name for i in random_set]
			form.save()

			return HttpResponseRedirect(reverse('home'))

	return render(request, 'home.html')

def base(request):
	sp_span = len(Species.objects.all())
	gen_span = len(Genus.objects.all())
	subclass_span = len(Subclass.objects.all())
	books_span = len(Book.objects.all())
	points_span = len(TaxonOnMap.objects.all())


	context = {'sp_span': sp_span, 'gen_span': gen_span, 'books_span': books_span,
			'points_span': points_span, 'subclass_span': subclass_span}
	return render(request, 'base.html', context)

def base_settings(request):
	taxons = (Division, Class, Subclass, Order, Family, Genus, Species)
	search_query = request.GET.get('search', '')
	taxons_list = []
	bad_request = 'К сожалению, по Вашему запросу ничего не найдено. Проверьте запрос.'

	if search_query:
		for taxon in taxons:
			search = taxon.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
			if search:
				taxons_list.append(search)
	else:
		for taxon in taxons:
				tax = taxon.objects.all()
				if len(tax) > 0:
					taxons_list.append(tax)
				else:
					pass

	context = {'search_query': search_query, 'taxons_list': taxons_list, 'bad_request': bad_request}
	return render(request, 'taxons_list.html', context)


#универсальная функция для обработки объекта любой модели
def universal_taxon(request, name):
	obj = TaxonFinder(name=name)
	taxon = obj.taxon_object() #поиск объекта среди всех классов таксонов
	tax = obj.taxon_model() #определение названия класса, содежащего в себе этот объект
	images = obj.taxon_images() #связанные с объектом изображения
	bounds = obj.taxon_bounds() #имеющие объект в атрибуте с ForeignKey

	return render(request, 'universal_taxon.html', {'taxon': taxon, 'images': images})


def all_taxons(request):
	'''Все таксоны'''
	models_list = (Division, Class, Subclass, Order, Family, Genus, Species)
	taxons = []
	for model in models_list:
		taxons2 = list(lambda model: model.objects.all() for model in models_list)
	for model in models_list:
		tax = model.objects.all()
		if len(tax) > 0:
			taxons.append(tax)
		else:
			pass

	return render(request, 'all_taxons.html', {'taxons': taxons})

def edition(request, name):
	'''Универсальная функция для редактирования записей относящихся к любой модели'''
	taxons_list = (Division, Class, Subclass, Order, Family, Genus, Species)
	taxon = None
	tax = None
	for tax in taxons_list:
		try:
			taxon = tax.objects.get(name=str(name))
			tax = tax
		except:
			pass
	if not taxon == None:
		class EditionForm(forms.ModelForm):
			class Meta:
				model = tax
				fields = '__all__'
				exclude = ['creator', 'parent_taxon']

			images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)


		form = EditionForm(instance=taxon)
		if request.method == 'POST':
			form = EditionForm(request.POST, request.FILES, instance=taxon)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('taxons:universal_taxon', args=(taxon.name,)))
	print(taxon.parent_taxon)
	return render(request, 'edition.html', {'form': form, 'taxon': taxon})
	
def species_list(request):
	'''Совокупность функций для вывода все объектов одного из классов - всех видов, всех родов и тд.'''
	taxons_list = Species.objects.order_by('name')

	context = {'taxons_list': taxons_list}
	return render(request, 'taxons_list.html', context)

def genus_list(request):
	taxons_list = Genus.objects.order_by('name')

	return render(request, 'taxons_list.html', {'taxons_list': taxons_list})

def family_list(request):
	taxons_list = Family.objects.order_by('name')

	return render(request, 'taxons_list.html', {'taxons_list': taxons_list})

def order_list(request):
	taxons_list = Order.objects.order_by('name')

	return render(request, 'taxons_list.html', {'taxons_list': taxons_list})

def subclass_list(request):
	taxons_list = Subclass.objects.order_by('name')

	return render(request, 'taxons_list.html', {'taxons_list': taxons_list})

def class_list(request):
	taxons_list = Class.objects.order_by('name')

	return render(request, 'taxons_list.html', {'taxons_list': taxons_list})

def class_list(request):
	taxons_list = Class.objects.order_by('name')

	return render(request, 'taxons_list.html', {'taxons_list': taxons_list})

def division_list(request):
	taxons_list = Division.objects.order_by('name')

	return render(request, 'taxons_list.html', {'taxons_list': taxons_list})

def new_taxon(request):
	'''Создание нового объекта одного из классов в иерархии таксонов. Чтоб не делать для каждого класса отдельную
	функцию, я придумал так: пользователь вводит данные в форму не связанную с моделью, а затем они передаются
	в форму связанную с моделью - название модели берется из атрибута rank первой формы, который выбирает пользователь. Возможно, чрезмерно мудреная функция, но очень хотелось сделать одну универсальную, вместо
	большого количества однотипных'''
	taxons = [(i.identifier, i.name) for i in Taxa.objects.all()] #Спиок с названиями всех классов для создания новых записей
	class NewTaxon(forms.Form):
		rank = forms.CharField(label='Выберите ранг растения', widget=forms.RadioSelect(choices=taxons))
		name = forms.CharField(label='Название')
		description = forms.CharField(label='Описание таксона', widget=forms.Textarea(), required=False)
		definer_description = forms.CharField(label='Описание таксона для определителя', widget=forms.Textarea(), required=False)
		images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)

	taxons_list = (Division, Class, Subclass, Order, Family, Genus, Species)
	form = NewTaxon()
	if request.method == 'POST':
		form = NewTaxon(request.POST, request.FILES)
		if form.is_valid():
			rank_type = form.cleaned_data['rank']
			for taxon in taxons_list:
				if rank_type == taxon.__name__:
					#parent_taxon = taxons_list[taxons_list.index(taxon) - 1]
					#parents_list = [(i.name, i.name) for i in parent_taxon.objects.all()]

					#создание второй формы, в которую передадутся данные из первой
					class TaxonCreation(forms.ModelForm):
						class Meta:
							model = taxon
							fields =  '__all__'
							exclude = ['img']


					form = TaxonCreation()
					if request.method == 'POST':
						form = TaxonCreation(request.POST, request.FILES)
						if form.is_valid():
							form_name = form.cleaned_data['name']
							form = form.save(commit=False)
							form.creator = request.user
							form.parent_taxon = form.parent_taxon
							for i in Taxa.objects.all():
								if i.identifier == rank_type:
									try:
										taxa_name = Taxa.objects.get(name=i.name)
										form.tax = taxa_name
									except:
										pass

							form.save()

							new_object = taxon.objects.get(name=form_name)
							obj = TaxonFinder(name=form_name) #для определения в след.строке названия класса с изображениями
							model_name = obj.taxon_images_model()

							#загрузка множественных изображений
							for f in request.FILES.getlist('images'):
								data = f.read()
								image_obj = model_name(taxon=new_object)
								image_obj.image.save(f.name, ContentFile(data))
								image_obj.save()

							return HttpResponseRedirect(reverse('taxons:universal_taxon', args=(form_name,)))



	return render(request, 'new_taxon.html', {'form': form})

def multiple_images(request, taxon_name):
	'''TaxonFinder - класс содержащий функции для нахождения по уникальному имени объекта 
	среди всех моделей, на основе которых создаются таксоны 
	taxon_object() находит нужный объект, а taxon_model() возвращает название модели, от которой он происходит'''
	obj = TaxonFinder(name=taxon_name)
	taxon = obj.taxon_object()
	tax = obj.taxon_model()
	form = AddMultipleImages()
	model_name = obj.taxon_images_model()

	if request.method == 'POST':
		form = AddMultipleImages(request.POST, request.FILES)
		if form.is_valid():

			for f in request.FILES.getlist('images'):
				data = f.read()
				photo = model_name(taxon=taxon)
				photo.image.save(f.name, ContentFile(data))
				photo.save()
			return HttpResponseRedirect(reverse('taxons:universal_taxon', args=(taxon.name,)))

	return render(request, 'multiple_images.html', {'form': form, 'taxon': taxon})


def main_image(request, taxon_name):
	'''Выбор главного изображения, которое будет аватаром записи'''
	obj = TaxonFinder(name=taxon_name)
	taxon = obj.taxon_object()
	tax = obj.taxon_model()
	images  = list(obj.taxon_images())
	list_images = [(i.image, images.index(i)+1) for i in images]
	#список всех связанных с объектом изображений
	#форма в теле функции для того, чтоб передать атрибут model класс таксона; вроде бы все работает :)
	class MainImage(forms.ModelForm):
		class Meta:
			model = tax
			fields = ['img']

	form = MainImage(instance=taxon)
	form.fields['img'] = forms.ChoiceField(choices=list_images)

	if request.method == 'POST':
		form = MainImage(request.POST, instance=taxon)
		form.fields['img'] = forms.ChoiceField(choices=list_images)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('taxons:universal_taxon', args=(taxon.name,)))

	return render(request, 'main_image.html', {'form': form, 'taxon': taxon, 'list_images': list_images, 'images':images})


@allowed_users(allowed_roles=['admin'])
def delete_taxon(request, taxon_name):
	'''Удаление объекта; перед удалением проверяется его наличие в списке объектов отобранных для вывода 
	   их изображений на главной странице; если объект находится в списке, то его название удаляется из него, что позволяет избежать ошибки при попытке вывести уже удаленное изображение объекта, все еще содержащегося в списке случайно отобранных для вывода на главной странице объектов'''
	obj = TaxonFinder(name=taxon_name)
	taxon = obj.taxon_object()

	if request.method == 'POST':
		#далее проверка нахождения удаляемого объекта в списке
		homepage_images = HomepageImages.objects.get(id=1)
		form = HomepageImagesForm(request.POST, instance=homepage_images)
		img_list = homepage_images.img_field
		search = re.search(taxon.name, img_list)
		if not search == None:
			del_obj = (f'\'{taxon.name}\', ', f', \'{taxon.name}\'')
			for i in del_obj:
				new_line = re.sub(i, '', img_list)
				test = re.search(taxon.name, new_line)
				if test == None:
					form.img_field = new_line
					form.save()

		taxon.delete()
		return HttpResponseRedirect(reverse('taxons:all_taxons'))

	context = {'taxon': taxon}
	return render(request, 'delete_taxon.html', context)

def profile_page(request):
	taxons_list = (Division, Class, Subclass, Order, Family, Genus, Species)
	user = request.user
	user_custom = request.user.profile
	points = TaxonOnMap.objects.filter(creator=user)
	added_entry = [(i for i in taxon.objects.filter(creator=user)) for taxon in taxons_list]

	context = {'user': user, 'user_custom': user_custom, 'points': points, 'added_entry': added_entry}
	return render(request, 'profile.html', context)

def login_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username or password is incorrect')

	context  = {}
	return render(request, 'login.html', context)

def edit_profile(request):
	user_custom = request.user.profile

	form = UpdateUser(instance=user_custom)
	if request.method == 'POST':
		form = UpdateUser(request.POST, request.FILES, instance=user_custom)

		if form.is_valid():
			form.save()
			return redirect('profile_page')

	context = {'user_custom': user_custom, 'form': form}
	return render(request, 'edit_profile.html', context)

def register(request):
	form = CreateUser()

	if request.user.is_authenticated:
		return HttpResponse('You should logout first')

	else:
		form = CreateUser()
		if request.method == 'POST':
			form = CreateUser(request.POST)
			if form.is_valid():
				new_user = form.save()
				username = form.cleaned_data.get('username')
				new_user.save()

				messages.success(request, 'You have succesfully made profile. Glad to see, ' + username)
				return redirect('home')

	context = {'form': form}
	return render(request, 'registration.html', context)

def logout_page(request):
	logout(request)
	return redirect('home')

def search(request):
	'''Поиск среди всех записей растений. Реализован неточный поиск - ищущий все совпадения введенных сиволов в названиях и описаниях растений, и точный - ищущий лишь точные совпадения'''
	myFilter = OrderFilter(request.GET)
	taxons = []
	bad_request = 'К сожалению, по Вашему запросу ничего не найдено. Проверьте запрос.'

	taxons_list = (Division, Class, Subclass, Order, Family, Genus, Species)
	search_query = request.GET.get('inexact_search', '')
	if search_query:
		for taxon in taxons_list:
			search = taxon.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
			taxons.append(search)
	elif myFilter:
		species = []
		for taxon in taxons_list:
			myFilter = OrderFilter(request.GET, queryset=taxon.objects.order_by('name'))
			taxons.append(myFilter.qs)
	else:
		pass

	context = {'taxons': taxons, 'myFilter': myFilter, 'bad_request': bad_request}


	return render(request, 'search.html', context)

def book(request, book_id):
	'''Скачать книгу'''
	book_obj = Book.objects.get(id=book_id)
	book_obj.counter += 1
	book_obj.save()
	return redirect(book_obj.file.url)

def book_add(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
        	form.save()
       		return redirect('home')
    else:
    	form = UploadFileForm()

    context = {'form': form}
    return render(request, 'book_add.html', context)

def books(request):
	'''Список всех книг'''
	all_books = Book.objects.all()

	return render(request, 'books.html', {'all_books': all_books})

def to_map(request):
	'''Открывает карту, на которой имеются отметки с наблюдениями'''
	map = folium.Map(location=[59.9453399167, 30.4518636944], zoom_start = 5)

	cluster = MarkerCluster().add_to(map)
	all_points = TaxonOnMap.objects.all()
	for point in all_points:
		tooltip = point.name
		html = '''
		<h3>''' + point.name + '''</h3><h4>''' + point.comment + '''</h4>'''
		iframe = IFrame(html=html, height=120, width=130)
		popup = folium.Popup(iframe, max_width=650)
		

		folium.Marker(location=[point.lat, point.lon], popup = popup, tooltip=tooltip,
			icon=folium.Icon(icon='cloud', color = 'green')).add_to(cluster)
	BASE_DIR = Path(__file__).resolve().parent.parent
	map.save(os.path.join(BASE_DIR, 'map4.html'))
	return render(request, 'map4.html')

def add_point(request):
	'''Добавить новое наблюдение на карту'''
	form = AddMossPoint()
	if request.method == 'POST':
		form = AddMossPoint(request.POST, request.FILES)
		if not request.FILES:
			if form.is_valid():
				name = form.cleaned_data['name']
				lat = form.cleaned_data['lat']
				lon = form.cleaned_data['lon']
				img = form.cleaned_data['image']
				new_marker(name, lat, lon, img)
			
				try:
					species = Species.objects.get(name=name)
					rel_form = form.save(commit=False)
					rel_form.relation = species
					rel_form.creator = request.user
					rel_form.save()
				except:
					rel_form = form.save(commit=False)
					rel_form.creator = request.user
					rel_form.save()
		elif request.FILES:
			if form.is_valid():
				form.image = form.cleaned_data['image']
				file = request.FILES['image']
				data = gpsphoto.getGPSData(str(file.temporary_file_path()))
				name = form.cleaned_data['name']
				lat = data.get('Latitude')
				lon = data.get('Longitude')
				img = form.cleaned_data['image']
				new_marker(name, lat, lon, img)

				try:
					species = Species.objects.get(name=name)
					rel_form = form.save(commit=False)
					rel_form.lat = lat
					rel_form.lon = lon
					rel_form.relation = species
					rel_form.creator = request.user
					rel_form.save()
				except:
					rel_form = form.save(commit=False)
					rel_form.lat = lat
					rel_form.lon = lon
					rel_form.relation = None
					rel_form.creator = request.user
					rel_form.save()
			return redirect('to_map')

	return render(request, 'add_point_on_map.html', {'form': form})

def points_list(request):
	'''Список наблюдений'''
	user = request.user

	points = TaxonOnMap.objects.all()
	points2 = TaxonOnMap.objects.filter(creator=user)

	context = {'points': points, 'points2': points2, 'user': user}
	return render(request, 'points_list.html', context)

def point_page(request, point_id):
	'''Страница с конкретным наблюдением'''
	point = TaxonOnMap.objects.get(id=point_id)

	return render(request, 'point_page.html', {'point': point})
