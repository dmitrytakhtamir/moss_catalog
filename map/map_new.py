import folium
from folium.plugins import MarkerCluster
import pandas as pd
import os
from folium import IFrame
from folium.plugins import FloatImage

import base64

map = folium.Map(location=[37.296933,-121.9574983], zoom_start = 3)
logoIcon = folium.features.CustomIcon('ptilium.jpg', icon_size=(35, 35))
tooltip = 'Click on me :)'

file =  'ptilium.jpg'
dir_base = os.getcwd()
Filename = dir_base + "/" + file
print(dir_base)
encoded = base64.b64encode(open(Filename, 'rb').read())

svg = """
<object data="data:image/jpg;base64,{}" width="{}" height="{} type="image/svg+xml">
</object>""".format
width, height, fat_wh = 250, 300, 1.3
html = '''<h3>Ptilium Crista-Castrensis</h3>
'''.format #<br><img src="data:image/JPG;base64,{}"><br>
html = html(encoded.decode('UTF-8'), width, height) + svg(encoded.decode('UTF-8'), width, height)
iframe = IFrame(html=html , width=width*fat_wh, height=height*fat_wh)
#iframe = IFrame(svg(encoded.decode('UTF-8'), width, height) , width=width*fat_wh, height=height*fat_wh)
popup  = folium.Popup(iframe, parse_html = True)

folium.Marker(location=[45.8797989,-122.0810013], popup=popup, tooltip=tooltip).add_to(map)

folium.CircleMarker(
	location = [45.9297981,-121.8209991], 
	radius=50,
	popup='searching area',
	color='#428bca',
	fill=True,
	fill_color='#428bca'
	).add_to(map)

#начальная и конечные точки должны совпадать
point_list = [[50.854457,4.377184],[52.518172,13.407759], [50.072651,14.435935], [48.853033,2.349553], [50.854457,4.377184]]
folium.Polygon(locations=point_list, color="green", fill_color='blue', weight=2.5, opacity=1).add_to(map)

map.save('map5.html')