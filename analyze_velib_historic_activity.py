from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium

def plot_stations_sorted_by_activity(path):
    df = pd.read_csv(path)
    
    # Order the stations by total_activity before plotting them
    df_sorted = df.sort_values(by='total_activity', ascending=False).reset_index(drop=True)

    # Plot all the stations on the x axis with activity on the y axis
    plt.figure(figsize=(10, 6))
    plt.bar(df_sorted.index, df_sorted['total_activity'])
    plt.xlabel('Stations')
    plt.ylabel('Activity')
    plt.title('Velib Station Activity sorted by Activity')
    plt.xticks([],[])

    # Add a linear trend line
    z = np.polyfit(range(len(df_sorted)), df_sorted['total_activity'], 1)
    p = np.poly1d(z)
    plt.plot(range(len(df_sorted)), p(range(len(df_sorted))), "r--")
    # Add the slope of the trendline to the graph
    slope = z[0]
    plt.text(0.05, 0.95, f'Slope: {slope:.2f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.savefig('output/activity_of_stations_sorted_by_activity.png')

def plot_stations_sorted_by_opening(path):
    df = pd.read_csv(path)
    # Filter for stations which have dateOuverture
    print(f"Total stations: {len(df)}")
    df_filtered = df[df['dateOuverture'].notna()]
    print(f"Stations with matched opening date: {len(df_filtered)}")
    # df_filtered = df_filtered[df_filtered['dateOuverture'] < '2018-04-01']
    # print(f"Stations with opening date before 2018 Q2: {len(df_filtered)}")

    # Order the stations by dateOuverture before plotting them
    df_sorted = df_filtered.sort_values(by='dateOuverture').reset_index(drop=True)

    # Plot all the stations on the x axis with dateOuverture on the y axis
    plt.figure(figsize=(10, 6))
    # Green for stations opened in 2018 Q1, blue for stations opened after
    colors = ['green' if datetime.strptime(date, '%Y-%m-%d') < datetime(2018, 4, 1) else 'blue' for date in df_sorted['dateOuverture']]
    plt.bar(df_sorted.index, df_sorted['total_activity'], color=colors)
    plt.xlabel('Stations')
    plt.ylabel('Activity')
    plt.title('Velib Station Activity sorted by Opening Date')
    plt.xticks([],[])

    # Add a linear trend line
    z = np.polyfit(range(len(df_sorted)), df_sorted['total_activity'], 1)
    p = np.poly1d(z)
    plt.plot(range(len(df_sorted)), p(range(len(df_sorted))), "r--")
    # Add the slope of the trendline to the graph
    slope = z[0]
    plt.text(0.05, 0.95, f'Slope: {slope:.2f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.savefig('output/activity_of_stations_sorted_by_opening.png')


from map_velib_all_stations import add_velib_stations
from helper_paris_map import get_paris_center

def plot_stations_from_both_sources_on_map(path):
    df = pd.read_csv(path)

    # Create a map centered around Paris
    m = folium.Map(get_paris_center(), zoom_start=12,control_scale=True)

    cutoff_date = datetime.strptime('2025-01-01', '%Y-%m-%d')
    add_velib_stations(cutoff_date, m)

    # Add a circular marker for each station
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=row['station_geo'].split(','),
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6,
            popup=f"Station: {row['station_name']}<br>Activity: {row['total_activity']}",
        ).add_to(m)

    # Save the map to an HTML file
    m.save('output/velib_merged_stations_map.html')

# Run code 

# Import data with specified header names
# (after processing and merging with process_velib_historic_station_activity.py is done)
path = 'data/velib-merged-station-data.csv'

plot_stations_sorted_by_activity(path)
plot_stations_sorted_by_opening(path)
# plot_stations_from_both_sources_on_map(path)



