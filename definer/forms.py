from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User

class SearchCreation(forms.ModelForm):
	class Meta:
		model = TaxonSearch
		fields = '__all__'