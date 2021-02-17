
'''def cards_choice(request):
	search_cards = TaxonSearch.objects.all()
	class CardChoice(forms.Form):
		cards = [[i, i] for i in search_cards]
		print(cards)

		choice_field = forms.CharField(label='Выберите карточку', widget=forms.RadioSelect(choices=cards))

	choice_form = CardChoice()
	if request.method == 'POST':
		choice_form = CardChoice(request.POST)
		if choice_form.is_valid():

			return HttpResponseRedirect(reverse('definer:activation', args(14)))

	return render(request, 'definer_subclass.html', {'choice_form': choice_form})
'''
def activation22(request, card_id):
	if TaxonSearch.objects.get(id=card_id):
		card = TaxonSearch.objects.get(id=card_id)
		all_cards =  TaxonSearch.objects.all()

		form = SearchCreation(instance=card)
		if request.method == 'POST':
			form = SearchCreation(request.POST, instance=card)
			subclass = card.subclass
			order = card.order
			family = card.family
			genus = card.genus
			species = card.species
			if form.is_valid():
				if card.activation == 'Act':
					form = form.save(commit=False)
					form.activation = 'Deact'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()
					return redirect('definer:definer_subclass')
				elif card.activation == 'Deact'  or card.activation == None  or card.activation == 'Frozen':
					form = form.save(commit=False)
					form.activation = 'Act'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()

					for card_obj in all_cards:
						if card_obj.id != card.id and card_obj.activation == 'Act':
							subclass = card_obj.subclass
							order = card_obj.order
							family = card_obj.family
							genus = card_obj.genus
							species = card_obj.species
							form2 = SearchCreation(request.POST, instance=card_obj)
							if form2.is_valid():
								form2 = form2.save(commit=False)
								form2.activation = 'Deact'
								form2.subclass, form2.order, form2.family, form2.genus, form2.species = subclass, order, family, genus, species

								form2.save()
					return redirect('definer:definer_subclass')
	else:
		pass


	return render(request, 'definer_subclass.html', {'form': form})

def activation21(request, card_id):
	print("HELLOact")
	if TaxonSearch.objects.get(id=card_id):
		card = TaxonSearch.objects.get(id=card_id)
		all_cards =  TaxonSearch.objects.all()

		form = SearchCreation(instance=card)
		if request.method == 'POST':
			form = SearchCreation(request.POST, instance=card)
			print(card.subclass)
			subclass = card.subclass
			order = card.order
			family = card.family
			genus = card.genus
			species = card.species
			if form.is_valid():
				if card.activation == 'Act':
					form = form.save(commit=False)
					form.activation = 'Deact'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()
					return redirect('definer:cards_list')
				if card.activation == 'Deact'  or card.activation == None  or card.activation == 'Frozen':
					form = form.save(commit=False)
					form.activation = 'Act'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()

					for card_obj in all_cards:
						if card_obj.id != card.id and card_obj.activation == 'Act':
							subclass = card_obj.subclass
							order = card_obj.order
							family = card_obj.family
							genus = card_obj.genus
							species = card_obj.species
							form2 = SearchCreation(request.POST, instance=card_obj)
							if form2.is_valid():
								form2 = form2.save(commit=False)
								form2.activation = 'Deact'
								form2.subclass, form2.order, form2.family, form2.genus, form2.species = subclass, order, family, genus, species

								form2.save()
					return redirect('definer:cards_list')
	else:
		pass


	return render(request, 'cards_list.html', {'form': form})

def activation_in_unitaxon2(request, taxon_name, card_id):
	print('HELLOactUni')
	if TaxonSearch.objects.get(id=card_id):
		card = TaxonSearch.objects.get(id=card_id)
		all_cards = TaxonSearch.objects.all()
		obj = TaxonFinder(name=taxon_name)
		taxon = obj.taxon_object()

		form = SearchCreation(instance=card)
		if request.method == 'POST':
			form = SearchCreation(request.POST, instance=card)
			subclass = card.subclass
			order = card.order
			family = card.family
			genus = card.genus
			species = card.species
			if form.is_valid():
				if card.activation == 'Act':
					form = form.save(commit=False)
					form.activation = 'Deact'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()
					return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(taxon.name,)))
				if card.activation == 'Deact'  or card.activation == None or card.activation == 'Frozen':
					form = form.save(commit=False)
					form.activation = 'Act'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()

					for card_obj in all_cards:
						if card_obj.id != card.id and card_obj.activation == 'Act':
							subclass = card_obj.subclass
							order = card_obj.order
							family = card_obj.family
							genus = card_obj.genus
							species = card_obj.species
							form2 = SearchCreation(request.POST, instance=card_obj)
							if form2.is_valid():
								form2 = form2.save(commit=False)
								form2.activation = 'Deact'
								form2.subclass, form2.order, form2.family, form2.genus, form2.species = subclass, order, family, genus, species

								form2.save()
					return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(taxon.name,)))
	else:
		pass


	return render(request, 'definer_unitaxon.html', {'form': form})

def card_freezing2(request, taxon_name, card_id):
	if TaxonSearch.objects.get(id=card_id):
		card = TaxonSearch.objects.get(id=card_id)
		all_cards = TaxonSearch.objects.all()
		obj = TaxonFinder(name=taxon_name)
		taxon = obj.taxon_object()

		form = SearchCreation(instance=card)
		if request.method == 'POST':
			form = SearchCreation(request.POST, instance=card)
			subclass = card.subclass
			order = card.order
			family = card.family
			genus = card.genus
			species = card.species
			if form.is_valid():
				if card.activation == 'Act' or card.activation == 'Deact':
					form = form.save(commit=False)
					form.activation = 'Frozen'
					button_name = 'Разморозить'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()
					return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(taxon.name,)))
				elif card.activation == 'Frozen':
					form = form.save(commit=False)
					form.activation = 'Act'
					button_name = 'Заморозить'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()

					for card_obj in all_cards:
						if card_obj.id != card.id and card_obj.activation == 'Act':
							subclass = card_obj.subclass
							order = card_obj.order
							family = card_obj.family
							genus = card_obj.genus
							species = card_obj.species
							form2 = SearchCreation(request.POST, instance=card_obj)
							if form2.is_valid():
								form2 = form2.save(commit=False)
								form2.activation = 'Deact'
								form2.subclass, form2.order, form2.family, form2.genus, form2.species = subclass, order, family, genus, species

								form2.save()
					return HttpResponseRedirect(reverse('definer:definer_unitaxon', args=(taxon.name,)))
	else:
		pass


	return render(request, 'definer_unitaxon.html')

def card_freezing_subclass2(request, card_id):
	if TaxonSearch.objects.get(id=card_id):
		card = TaxonSearch.objects.get(id=card_id)
		all_cards = TaxonSearch.objects.all()


		form = SearchCreation(instance=card)
		if request.method == 'POST':
			form = SearchCreation(request.POST, instance=card)
			subclass = card.subclass
			order = card.order
			family = card.family
			genus = card.genus
			species = card.species
			if form.is_valid():
				if card.activation == 'Act' or card.activation == 'Deact':
					form = form.save(commit=False)
					form.activation = 'Frozen'
					button_name = 'Разморозить'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()
					return HttpResponseRedirect(reverse('definer:definer_subclass'))
				elif card.activation == 'Frozen':
					form = form.save(commit=False)
					form.activation = 'Act'
					button_name = 'Заморозить'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()

					for card_obj in all_cards:
						if card_obj.id != card.id and card_obj.activation == 'Act':
							subclass = card_obj.subclass
							order = card_obj.order
							family = card_obj.family
							genus = card_obj.genus
							species = card_obj.species
							form2 = SearchCreation(request.POST, instance=card_obj)
							if form2.is_valid():
								form2 = form2.save(commit=False)
								form2.activation = 'Deact'
								form2.subclass, form2.order, form2.family, form2.genus, form2.species = subclass, order, family, genus, species

								form2.save()
					return HttpResponseRedirect(reverse('definer:definer_subclass'))
	else:
		pass


	return render(request, 'definer_subclass.html')

def cards_list_freezing2(request, card_id):
	if TaxonSearch.objects.get(id=card_id):
		card = TaxonSearch.objects.get(id=card_id)
		all_cards = TaxonSearch.objects.all()


		form = SearchCreation(instance=card)
		if request.method == 'POST':
			form = SearchCreation(request.POST, instance=card)
			subclass = card.subclass
			order = card.order
			family = card.family
			genus = card.genus
			species = card.species
			if form.is_valid():
				if card.activation == 'Act' or card.activation == 'Deact':
					form = form.save(commit=False)
					form.activation = 'Frozen'
					button_name = 'Разморозить'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()
					return HttpResponseRedirect(reverse('definer:cards_list'))
				elif card.activation == 'Frozen':
					form = form.save(commit=False)
					form.activation = 'Act'
					button_name = 'Заморозить'

					form.subclass, form.order, form.family, form.genus, form.species = subclass, order, family, genus, species

					form.save()

					for card_obj in all_cards:
						if card_obj.id != card.id and card_obj.activation == 'Act':
							subclass = card_obj.subclass
							order = card_obj.order
							family = card_obj.family
							genus = card_obj.genus
							species = card_obj.species
							form2 = SearchCreation(request.POST, instance=card_obj)
							if form2.is_valid():
								form2 = form2.save(commit=False)
								form2.activation = 'Deact'
								form2.subclass, form2.order, form2.family, form2.genus, form2.species = subclass, order, family, genus, species

								form2.save()
					return HttpResponseRedirect(reverse('definer:cards_list'))
	else:
		pass


	return render(request, 'cards_list.html')
