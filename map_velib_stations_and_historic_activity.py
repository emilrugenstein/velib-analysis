import pandas as pd
import folium
from datetime import datetime
from geopy.distance import geodesic
from folium.plugins import HeatMap
import branca.colormap as cm

from helper_paris_map import get_paris_boroughs, get_paris_center
from map_velib_all_stations import add_velib_stations

# Create a map centered around Paris
m = folium.Map(location=get_paris_center(), zoom_start=12)
get_paris_boroughs().add_to(m)

# filter stations to only include 2018 Q1
cutoff_date = datetime.strptime('2018-04-01', '%Y-%m-%d')

# add stations
add_velib_stations(cutoff_date, m)

# Load historic bike activity data
years = [2019]
bike_activity_data = []
for year in years:
    meters = pd.read_csv(f'data/{year}-comptage-velo-donnees-compteurs.csv', sep=';')
    grouped_meters = meters.groupby('site-id').agg({
        'hourly-metering': 'sum',
        'coordinates': 'first'
    }).reset_index()
    bike_activity_data.append(grouped_meters)

    for idx, row in grouped_meters.iterrows():
        if row['hourly-metering'] > 0:
            coordinates = [float(coord) for coord in row['coordinates'].split(',')]
            folium.CircleMarker(
            location=coordinates,
            radius=2,
            color='black',
            opacity=1,
            fill=True,
            fill_color='black'
            ).add_to(m)


bike_activity_data = pd.concat(bike_activity_data)

# Create a heatmap based on the historic bike activity data
heat_data = [
    [float(row['coordinates'].split(',')[0]), float(row['coordinates'].split(',')[1]), row['hourly-metering'] * (1/100)]
    for _, row in bike_activity_data.iterrows() if row['hourly-metering'] > 0
]
HeatMap(heat_data).add_to(m)

# Add a legend to the map
colormap = cm.LinearColormap(colors=['blue', 'lime', 'yellow', 'orange', 'red'], vmin=0, vmax=max([point[2] for point in heat_data])*100)
colormap.caption = 'Yearly Bike Traffic'
colormap.add_to(m)

# Get the HTML element of the legend and set the background to white
colormap.get_root().html.add_child(folium.Element("""
    <style>
        .legend {
            background-color: white;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
"""))

# Save the map to an HTML file
years_str = '_'.join(map(str, years))
m.save(f'output/velib_stations_and_historic_activity_map_{years_str}.html')