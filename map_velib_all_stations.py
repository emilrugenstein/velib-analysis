import json
import folium
from datetime import datetime

from helper_paris_map import get_paris_boroughs, get_paris_center

def add_velib_stations(cutoff_date, map):
    # Path to the Velib JSON file
    file_path = 'data/velib-nocel-stations-api-reponse.json'

    # Load Velib stations data
    with open(file_path) as file:
        velib_data = json.load(file)['data']

    # Filter Velib stations by date Ouverture
    filtered_stations = [station for station in velib_data if datetime.strptime(station['dateOuverture'], '%Y-%m-%d') < cutoff_date]

    print("count of filtered stations: ", len(filtered_stations))

    # Add markers for each station
    # Define a function to get color based on the month as a gradient from green to red
    def get_marker_color(date_str):
        month = datetime.strptime(date_str, '%Y-%m-%d').month
        year = datetime.strptime(date_str, '%Y-%m-%d').year
        # Gradient from green to red (12 colors for 12 months)
        colors = [
            'green', 'yellow', 'orange', 'red'
        ]
        
        if (year == 2018):
            return colors[int((month - 1)/ 3)] # 3 months per color
        elif (year == 2019):
            return "purple"
        else:
            return "black"

    for station in filtered_stations:
        lat = station['latitude']
        lon = station['longitude']
        color = get_marker_color(station['dateOuverture'])
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,  # size of the dot
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=station['name'] + ' ' + station['dateOuverture']
        ).add_to(map)

    return map

# Create a map centered around Paris
velib_map = folium.Map(location=get_paris_center(), zoom_start=12)
get_paris_boroughs().add_to(velib_map)

# filter stations by date Ouverture
cutoff_date = datetime.strptime('2026-01-01', '%Y-%m-%d')

# add stations
add_velib_stations(cutoff_date, velib_map)

# add a legend
# Define the legend's HTML (hardcoded for simplicity)
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 145px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white;">
     &nbsp; <i class="fa fa-circle" style="color:green"></i> &nbsp; 2018 Q1 - 508 added<br>
     &nbsp; <i class="fa fa-circle" style="color:yellow"></i> &nbsp; 2018 Q2 - 290 added<br>
     &nbsp; <i class="fa fa-circle" style="color:orange"></i> &nbsp; 2018 Q3 - 106 added<br>
     &nbsp; <i class="fa fa-circle" style="color:red"></i> &nbsp; 2018 Q4 - 142 added<br>
     &nbsp; <i class="fa fa-circle" style="color:purple"></i> &nbsp; 2019 (full) - 269 added<br>
     &nbsp; <i class="fa fa-circle" style="color:black"></i> &nbsp; after 2019 - 155 added<br>
      &nbsp; <i class="fa fa-square" style="color:grey"></i> &nbsp; Parisian Boroughs<br>
</div>
'''
# Add the legend to the map
velib_map.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
velib_map.save('output/velib_stations_map.html')

