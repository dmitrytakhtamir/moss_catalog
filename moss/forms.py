from django import forms
from .models import  *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User

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
		fields = ['title', 'file']

class AddMossPoint(forms.ModelForm):
	class Meta:
		model = TaxonOnMap
		fields = ['name', 'lat', 'lon', 'image', 'comment']

class HomepageImagesForm(forms.ModelForm):
	class Meta:
		model = HomepageImages
		fields = '__all__'

class AddMultipleImages(forms.Form):
	images = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}), required=False)



