from django.apps import AppConfig


class MossConfig(AppConfig):
    name = 'moss'

    def ready(self):
    	import moss.signals

