'''
This script pulls current 2-hour forecast from the Singapore's NEA API and
plots geospatially the 2-hour forecast
'''

import requests
import json
import os
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from datetime import datetime, timedelta
import logging 

from forecastfetch import ForecastFetch

def ForecastVisualise():
    CurrentForecastDF = ForecastFetch()
    # Visualisation script

    # Center the map over Singapore
    map_center = [1.3521, 103.8198]  # Approximate coordinates of Singapore

    # Create a Folium map
    m = folium.Map(location=map_center, zoom_start=12)

    # Prepare data for HeatMap
    heat_data = [[row['latitude'], row['longitude'], row['forecast']] for index, row in CurrentForecastDF.iterrows()]

    CurrentForecastDF['forecast'] = CurrentForecastDF['forecast'].astype(str)  # Ensure the column is float type

    # Reading of the SG geojson file
    script_dir = os.path.abspath(os.path.dirname(__file__))
    singapore_map = gpd.read_file(os.path.join(script_dir, 'MasterPlan2019PlanningAreaBoundaryNoSea.geojson'))

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the Singapore map
    singapore_map.plot(ax=ax, color='lightgray', edgecolor='darkgray')
    
    # Plotting the 2-hour forecasts for every township
    ## Plotting the positions of the townships and respective colours depending on forecast
    weights = CurrentForecastDF['weights'].astype(str)
    for category in CurrentForecastDF['category']:
        if category == 'dry':
              ax.scatter(CurrentForecastDF['longitude'], 
            CurrentForecastDF['latitude'], color = 'grey')
        else: # category == 'wet'
            ax.scatter(CurrentForecastDF['longitude'], 
            CurrentForecastDF['latitude'], cmap='Blues', c=weights)
    
    ## Looping through all townships and annotating the current forecast
    ## for that township
    for x, y, forecast in zip(CurrentForecastDF['longitude'],
                              CurrentForecastDF['latitude'],
                              CurrentForecastDF['forecast']):
         ax.annotate(forecast, xy=(x,y), xycoords='data',
                     xytext=(1.5,1.5), textcoords='offset points', 
                     size=5)


    # Set the title with the current timestamp
    valid_period = CurrentForecastDF['valid_period'].iloc[0]
    ax.set_title(f"Current Forecasts over Singapore from {valid_period}")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim([103.58, 104.1])
    ax.set_ylim([1.15, 1.50])

    plt.show()

if __name__ == '__main__':
     ForecastVisualise()

