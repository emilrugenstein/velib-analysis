import json
import pandas as pd
from geopy.distance import geodesic

# Processing raw data
def process_velib_historic_station_activity():
    # aproach inspired by [Florian Bergamasco](https://medium.com/@bergamasco.florian/the-importance-of-data-visualization-for-initiating-a-data-science-project-662fd8ac7093)

    # Import data with specified header names
    df = pd.read_csv('data/velib-historic-station-activity-raw.csv', header=None, names=['date', 'capacity', 'available_mechanical', 'available_electrical', 'station_name', 'station_geo', 'operative'])
    # print('df entries: ', len(df))

    # Filter the operating stations
    df = df[df['operative'] == True]

    # Convert the datetime column to datetime type
    df['datetime'] = pd.to_datetime(df['date'])

    # Extract the time, day, month and year from the datetime column
    df['hour'] = df['datetime'].dt.hour
    df['day'] = df['datetime'].dt.day
    df['month'] = df['datetime'].dt.month
    df['year'] = df['datetime'].dt.year
    df['weekday'] = df['datetime'].dt.weekday

    # Sort the DataFrame by station_geo and datetime
    df = df.sort_values(by=['station_geo', 'datetime'])

    # Group by station_geo and calculate the activity
    def calculate_activity(group):
        group = group.sort_values(by='datetime')
        group['mech_diff'] = group['available_mechanical'].diff().abs()
        group['elec_diff'] = group['available_electrical'].diff().abs()
        group['activity'] = group['mech_diff'].fillna(0) + group['elec_diff'].fillna(0)
        total_activity = group['activity'].sum()
        return pd.Series({
            'station_name': group['station_name'].iloc[0],
            'station_geo': group['station_geo'].iloc[0],
            'capacity': group['capacity'].iloc[0],
            'total_activity': total_activity,
            'count': len(group)
        })

    activity_df = df.groupby('station_geo').apply(calculate_activity).reset_index(drop=True)

    print(activity_df.head)

    # Save the processed data to a new CSV file
    activity_df.to_csv('data/velib-historic-station-activity-processed.csv', index=False)



# Merge with velib data station_geo to get the 'dateOuverture'
def merge_velib_historic_activity_with_opening_date():
    # Load processed Velib station activity data
    activity_df = pd.read_csv('data/velib-historic-station-activity-processed.csv')

    # Load Velib stations data from other data source
    file_path = 'data/velib-nocel-stations-api-reponse.json'
    with open(file_path) as file:
        velib_data = json.load(file)['data']
    # Convert Velib stations data to DataFrame
    velib_df = pd.DataFrame(velib_data)
    # Create 'station_geo' field by combining 'lat' and 'long'
    velib_df['station_geo'] = velib_df['latitude'].astype(str) + ',' + velib_df['longitude'].astype(str)

    # Merge the data with velib-nocel-stations-api-reponse.json based on geolocation to get the 'dateOuverture'
    # Not the most efficient way to do this, but it works
    def find_nearest_station(row, stations_df):
        # First, try to find a station with the same name
        same_name_station = stations_df[stations_df['name'] == row['station_name']]
        if not same_name_station.empty:
            return same_name_station.iloc[0].to_dict()

        # If no station with the same name is found, use the geocode approach
        min_distance = float('inf')
        nearest_station = None
        for _, station in stations_df.iterrows():
            station_coords = (station['latitude'], station['longitude'])
            row_coords = tuple(map(float, row['station_geo'].split(',')))
            distance = geodesic(row_coords, station_coords).meters
            if distance < min_distance and distance <= 150:
                min_distance = distance
                nearest_station = station
        return nearest_station.to_dict() if nearest_station is not None else None

    # Apply the function to find the nearest station within 150 meters
    activity_df['nearest_station'] = activity_df.apply(find_nearest_station, stations_df=velib_df, axis=1)

    # Extract the 'dateOuverture' from the nearest station
    activity_df['dateOuverture'] = activity_df['nearest_station'].apply(lambda x: x['dateOuverture'] if x is not None else None)

    # Drop the 'nearest_station' column
    merged_df = activity_df # .drop(columns=['nearest_station'])

    print(merged_df.head())

    print("check")

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv('data/velib-merged-station-data.csv', index=False)

# run code
# process_velib_historic_station_activity()
merge_velib_historic_activity_with_opening_date()
