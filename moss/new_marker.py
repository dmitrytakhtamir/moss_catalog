import folium
from folium.plugins import MarkerCluster
import os
from folium import IFrame
from folium.plugins import FloatImage
import base64

def new_marker(name, lat, lon, img):
	map = folium.Map(location=[59.9453399167, 30.4518636944], zoom_start = 5)
	tooltip = name
	file =  str(img)
	dir_base = os.getcwd()
	Filename = dir_base + '\\static\\images\\' + file
	print(str(Filename))
	encoded = base64.b64encode(open(Filename, 'rb').read())

	svg = """
	<object data="data:image/jpg;base64,{}" width="{}" height="{} type="image/svg+xml">
	</object>""".format
	width, height, fat_wh = 250, 300, 1.3
	html = '''<h3>{{name}}</h3>
	'''.format
	html = html(encoded.decode('UTF-8'), width, height) + svg(encoded.decode('UTF-8'), width, height)
	iframe = IFrame(html=html , width=width*fat_wh, height=height*fat_wh)
	popup  = folium.Popup(iframe, parse_html = True)

	folium.Marker(location=[lat, lon], popup = popup, 
		icon=folium.Icon(icon='cloud', color = 'green'), tooltip=tooltip).add_to(map)

	#folium.Marker(location=[lat, lon], popup = name, icon=folium.Icon(icon='cloud', color = 'green')).add_to(map)
	#map.save("C:/Pyenv/moss_catalog/moss/templates/map4.html")
"""
		marker_cluster = MarkerCluster().add_to(map)
	
		folium.CircleMarker(location=[lat, lon], popup = name, 
			icon = folium.Icon(icon='cloud'), fill_color='green, color='gray', fill_opacity = 0.9).add_to(marker_cluster)
	"""	
			
	#logoIcon = folium.features.CustomIcon('ptilium.jpg', icon_size=(50, 50))




