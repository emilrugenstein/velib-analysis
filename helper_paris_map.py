import folium
import json

def get_paris_center():
    return [48.8566, 2.3522]

def get_paris_boroughs():
    # Path to the GeoJSON file with the arrondissements/boroughs  boundaries
    # Retrieved from https://opendata.paris.fr/explore/dataset/arrondissements/information/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImFycm9uZGlzc2VtZW50cyIsIm9wdGlvbnMiOnsibG9jYXRpb24iOiIxMiw0OC44NTg4OSwyLjM0NjkyIiwiYmFzZW1hcCI6Imphd2cuc3RyZWV0cyJ9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoiY29sdW1uIiwiZnVuYyI6IkFWRyIsInlBeGlzIjoibl9zcV9hciIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6IiMyNjM4OTIifV0sInhBeGlzIjoibl9zcV9hciIsIm1heHBvaW50cyI6NTAsInNvcnQiOiIifV0sInRpbWVzY2FsZSI6IiIsImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9
    geojson_path = 'data/paris-arrondissements.geojson'

    # Load the arondissments data
    with open(geojson_path) as geojson_file:
        geojson_data = json.load(geojson_file)

    # Add the GeoJSON layer to the map with grey color
    return folium.GeoJson(
        geojson_data,
        name='geojson',
        style_function=lambda feature: {
            'fillColor': 'grey',
            'color': 'grey',
            'weight': 2,
            'fillOpacity': 0.25,
        }
    )
