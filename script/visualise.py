'''
This script plots out the current precipitation readings heatmap from the past 5 minutes geospatially and saves
a .png file which shows the precipitation intensity geospatial information over Singapore
'''
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

from datafetch import PrecipFetch

def Visualise():
    CurrentPrecipDF = PrecipFetch()

    # Visualisation script
    ## Plotting heatmap of precipitation during 1900H to 2000H period and animating the propagation of precipitation
    # Center the map over Singapore
    map_center = [1.3521, 103.8198]  # Approximate coordinates of Singapore

    # Create a Folium map
    m = folium.Map(location=map_center, zoom_start=12)

    # Prepare data for HeatMap
    heat_data = [[row['latitude'], row['longitude'], row['values']] for index, row in CurrentPrecipDF.iterrows()]

    # Add heatmap to the map
    HeatMap(heat_data).add_to(m)

    # Save the map to an HTML file
    # m.save("singapore_rainfall_intensity.html")
    CurrentPrecipDF['values'] = CurrentPrecipDF['values'].astype(float)  # Ensure the column is float type

    # Reading of the SG geojson file
    script_dir = os.path.abspath(os.path.dirname(__file__))
    singapore_map = gpd.read_file(os.path.join(script_dir, 'MasterPlan2019PlanningAreaBoundaryNoSea.geojson'))

    # Prepare the data for the heatmap animation
    time_groups = CurrentPrecipDF.groupby('timestamp')

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set color normalization based on the min and max rainfall intensity in your dataset
    norm = Normalize(vmin=CurrentPrecipDF['values'].min(), vmax=CurrentPrecipDF['values'].max())
    cmap = plt.cm.Blues  # Other colormaps that can be tried are 'viridis' or 'coolwarm'

    # Create a ScalarMappable object for the colorbar
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # We set an empty array since we will pass data to the colorbar later

    # Add the colorbar
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Rainfall Intensity recorded during the 5-minute interval (mm)")

    # Define the update function for each frame
    def update(frame):
        ax.clear()  # Clear the axis for the new frame
        
        timestamp, time_slice = frame
        
        # Plot the Singapore map
        singapore_map.plot(ax=ax, color='lightgray', edgecolor='darkgray')
        
        # Create the scatter plot for the current frame
        sc = ax.scatter(
            time_slice['longitude'], 
            time_slice['latitude'], 
            c=time_slice['values'],  # Color based on rainfall intensity
            s=time_slice['values'] * 20,  # Adjust size of the dots
            cmap=cmap, 
            norm=norm,  # Use the normalization set earlier
            alpha=0.7
        )
        
        # Set the title with the current timestamp
        ax.set_title(f"Rainfall Intensity at {timestamp}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_xlim([103.58, 104.1])
        ax.set_ylim([1.15, 1.50])
        
        # The colorbar remains fixed with the same range across all frames

    # Prepare the frames (grouped by timestamp)
    frames = [(timestamp, time_slice) for timestamp, time_slice in time_groups]

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False)

    plt.show()

if __name__ == '__main__':
    Visualise()
