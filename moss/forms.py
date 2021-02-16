from django import forms
from .models import  *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User

class NewSpecies(forms.ModelForm):
	class Meta:
		model = Species
		fields = '__all__'
		exclude = ['creator']

class NewGenus(forms.ModelForm):
	class Meta:
		model = Genus
		fields = '__all__'
		exclude =  ['creator']

class SpeciesEdition(forms.ModelForm):
	class Meta:
		model = Species
		fields = '__all__'

class GenusEdition(forms.ModelForm):
	class Meta:
		model = Genus
		fields = '__all__'

class SubclassEdition(forms.ModelForm):
	class Meta:
		model = Subclass
		fields = '__all__'
		exclude = ['creator']
	
	images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)


class NewSubclass(forms.ModelForm):
	class Meta:
		model = Subclass
		fields = '__all__'
		exclude =  ['creator']
		
	images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)



class AddMoreImg(forms.ModelForm):
	class Meta: 
		model =  SpeciesImages
		fields = '__all__'

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        label = {'username': 'name of user'}
        
class UpdateUser(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


class SearchForm(ModelForm):
	class Meta:
		model = Species
		fields = ['name']

class UploadFileForm(ModelForm):
	class Meta:
		model = Book
		fields = '__all__'

class AddMossPoint(forms.ModelForm):
	class Meta:
		model = TaxonOnMap
		fields = ['name', 'lat', 'lon', 'image', 'comment']

SUBCLASS_LIST = [('bryidae', 'Bryidae'), 
				('andreaeidae', 'Andreaeidae'), 
				('sphagnidae', 'Sphagnidae')]

class DefinerSubClass(forms.Form):
	radio_button = forms.CharField(label='Выберите соответствие для найденного Вами мха, чтоб определить его подкласс',
		widget=forms.RadioSelect(choices=SUBCLASS_LIST))

class Test(forms.Form):
	text = forms.CharField(label='some text for testing', widget=forms.TextInput(
														attrs={'placeholder': 'input text here'}))

class HomepageImagesForm(forms.ModelForm):
	class Meta:
		model = HomepageImages
		fields = '__all__'

class AddMultipleImages(forms.Form):
	images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)



