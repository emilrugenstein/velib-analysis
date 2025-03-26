import pandas as pd
import folium

from helper_paris_map import get_paris_boroughs, get_paris_center


# Create a map centered around Paris
m = folium.Map(location=get_paris_center(), zoom_start=12)
get_paris_boroughs().add_to(m)

years = [2016, 2017, 2018, 2019, 2020]
colors = [
        'green', 'yellow', 'orange', 'red', 'purple', 'black'
    ]

for year in years:
    #import data
    meters = pd.read_csv(f'data/{year}-comptage-velo-donnees-compteurs.csv', sep=';')
    #print(len(meters))

    # Group meters by site-id and sum up the hourly metering 
    # grouped_meters == sites
    grouped_meters = meters.groupby('site-id').agg({
        'hourly-metering': 'sum',
        'coordinates': 'first',  # Assuming coordinates are the same for the same meter-id
    }).reset_index()
    print(len(grouped_meters))

    # Count how many sites have a sum higher than zero
    count_higher_than_zero = grouped_meters[grouped_meters['hourly-metering'] > 0].shape[0]
    print(f"Number of sites with a sum higher than zero in {year}: {count_higher_than_zero}")

    # Add grouped measurement points to the map
    for idx, row in grouped_meters.iterrows():
        coordinates = row['coordinates'].split(',')
        folium.CircleMarker(
            location=[float(coordinates[0]), float(coordinates[1])],
            radius= 1 + (row['hourly-metering'] ** 0.5) / 20, # quadratic scaling!
            color= colors[years.index(year)],
            fill=True,
            fill_color= colors[years.index(year)],
            popup=f"year: {year}, total: {row['hourly-metering']}, site-id: {row['site-id']}"
        ).add_to(m)

# Save the map to an HTML file
m.save('output/historic_bike_activity_map.html')

