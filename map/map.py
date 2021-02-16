import folium
from folium.plugins import MarkerCluster
import pandas as pd

data = pd.read_csv('Volcaenos_USA.txt')
lat  = data['LAT']
lon = data['LON']
elevation = data['ELEV']

def color_change(elev):
    if(elev < 1000):
        return('green')
    elif(1000 <= elev <3000):
        return('orange')
    else:
        return('red')

map = folium.Map(location=[37.296933,-121.9574983], zoom_start = 6, tiles= "CartoDB dark_matter")
map = folium.Map(location=[37.296933,-121.9574983], zoom_start = 6)
logoIcon = folium.features.CustomIcon('ptilium.jpg', icon_size=(50, 50))
marker_cluster = MarkerCluster().add_to(map)

for lat, lon, elevation in zip(lat, lon, elevation):
	folium.CircleMarker(location=[lat, lon], radius=9, popup = str(elevation) + ' m', 
		icon = folium.Icon(icon='cloud'),
		fill_color=color_change(elevation), color='gray', fill_opacity = 0.9, tooltip = 'Volcaeno')
		.add_to(marker_cluster)



map.save("map3.html")