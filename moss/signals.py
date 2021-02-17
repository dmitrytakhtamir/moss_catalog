from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import *
from django.db.models.signals import post_save

def create_profile(sender, instance, created, **kwargs):
	if created:

		group = Group.objects.get(name='profile')
		instance.groups.add(group)
		Profile.objects.create(user=instance, name=instance.username,)

		

post_save.connect(create_profile, sender=User)

def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.profile.save()

post_save.connect(update_profile, sender=User)