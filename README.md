# Analysis Velib
This project is part of a research essay which analyses the transition between different operators of the bike-sharing program called Velib in Paris.

## Output
Please see the "/output" folder for html files containing interactive maps 

Most notable are:
- "velib_stations_map.html" with an overview of all stations, colored based on when they were (re-)opened after 2017
- "velib_stations_and_historic_activity_map_2019.html" mapping stations opened in Q1 2018 onto a heatmap based on public bike traffic metering
- two PNG graphs which display activity/usage level of the stations ordered optimally vs. the real opening order after 2017

## Data Sources
Data about Velib bike docking stations: 
- retrieved from https://velib.nocle.fr/index.php
- based on opendata.paris.fr but also provides the opening date of each station

General bike traffic data:
- retrieved from https://opendata.paris.fr/explore/dataset/comptage-velo-historique-donnees-compteurs
- historic data about bike metering from the city of Paris

Velib station activity data:
- retrieved from https://github.com/lovasoa/historique-velib-opendata
- repasitory which recorded available bikes per station every 15min from 26.11.2020 until 09.04.2021

