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
    ## Mapping between forecasts and colour
    ForecastDict = {}

    ## Plotting heatmap of precipitation during 1900H to 2000H period and animating the propagation of precipitation
    # Center the map over Singapore
    map_center = [1.3521, 103.8198]  # Approximate coordinates of Singapore

    # Create a Folium map
    m = folium.Map(location=map_center, zoom_start=12)

    # Prepare data for HeatMap
    heat_data = [[row['latitude'], row['longitude'], row['forecast']] for index, row in CurrentForecastDF.iterrows()]


    # Save the map to an HTML file
    # m.save("singapore_rainfall_intensity.html")
    CurrentForecastDF['forecast'] = CurrentForecastDF['forecast'].astype(str)  # Ensure the column is float type

    # Reading of the SG geojson file
    singapore_map = gpd.read_file('NationalMapPolygonKML.geojson')

    # Prepare the data for the heatmap animation
    time_groups = CurrentForecastDF.groupby('timestamp')

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define the update function for each frame
    def update(frame):
        ax.clear()  # Clear the axis for the new frame
        
        timestamp, time_slice = frame
        
        # Plot the Singapore map
        singapore_map.plot(ax=ax, color='lightgray', edgecolor='lightgray')
        
        # Create the scatter plot for the current frame
        sc = ax.scatter(
            time_slice['longitude'], 
            time_slice['latitude'], 
            alpha=0.7
        )

        for xi, yi, text in zip(time_slice['longitude'], time_slice['latitude'], CurrentForecastDF['forecast']):
                ax.annotate(text,
                xy=(xi, yi), xycoords='data',
                xytext=(1.5, 1.5), textcoords='offset points', size=5)
        
        # Set the title with the current timestamp
        ax.set_title(f"Rainfall Intensity at {timestamp}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_xlim([103.58, 104.1])
        ax.set_ylim([1.15, 1.50])
        
    # Prepare the frames (grouped by timestamp)
    frames = [(timestamp, time_slice) for timestamp, time_slice in time_groups]

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False)

    # Save the animation as a gif or mp4
    ani.save("rainfall_animation_with_colorbar.png", writer='imagemagick', fps=1)

    # To save as mp4
    # ani.save("rainfall_animation_with_colorbar.mp4", writer='ffmpeg', fps=2)

    plt.show()

if __name__ == '__main__':
     ForecastVisualise()

