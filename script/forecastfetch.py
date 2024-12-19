'''
This script pulls current 2-hour forecast from the Singapore's NEA API and
packages it into a nice Pandas DataFrame.
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
# from alive-progress import alive_bar; import time

def ForecastFetch():

    def MetadataDF_Constructor(metadata: list):
        data = {'name': [], 'latitude': [], 'longitude': []}
        for dict in metadata:
            data['name'].append(dict['name'])
            data['latitude'].append(dict['label_location']['latitude'])
            data['longitude'].append(dict['label_location']['longitude'])
        return pd.DataFrame(data=data)

    logging.basicConfig(level=logging.INFO)

    url = 'https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast'
    response = requests.get(url)
    rawdata = response.json()
    forecast = rawdata['data']['items'][0]['forecasts'] # List of all forecasts
    update_timestamp = rawdata['data']['items'][0]['update_timestamp'] # String
    valid_period = rawdata['data']['items'][0]['valid_period']['text'] # String

    # Constructing the Metadata Dataframe
    metadata = rawdata['data']['area_metadata']
    MetaData = MetadataDF_Constructor(metadata)

    # Filling in the pulled data into a dataframe called CurrentForecastDF
    AreaList = [dict['area'] for dict in forecast]
    ForecastList = [dict['forecast'] for dict in forecast]
    timestampList = [update_timestamp for dict in forecast]
    valid_periodList = [valid_period for dict in forecast]
    
    # Grouping all data to either 'wet' or 'dry' according to the forecast value
    forecastvalues = pd.read_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'misc', 'forecastvalues.csv'))
    categoryList = [forecastvalues[forecastvalues['forecast'] == forecast]['category'].iloc[0] for forecast in ForecastList]

    data = {'timestamp': timestampList, 'area': AreaList, 'forecast': ForecastList, 'valid_period': valid_periodList, 'category': categoryList}
    CurrentForecastDF = pd.DataFrame(data=data)

    # Adding coordinate information into CurrentForecastDF
    new_df = pd.DataFrame(columns=['timestamp', 'area', 'forecast', 'valid_period', 'category', 'latitude', 'longitude'])
    for Forecastmetadf_row in MetaData.iterrows():
        for Forecastdf_row in CurrentForecastDF.iterrows():
            if Forecastmetadf_row[1]['name'] == Forecastdf_row[1]['area']:
                latlongseries = pd.Series(data=[Forecastmetadf_row[1]['latitude'], Forecastmetadf_row[1]['longitude']], index=['latitude', 'longitude'])
                Forecastdf_row = pd.concat([Forecastdf_row[1], latlongseries])
                new_df = pd.concat([new_df, pd.DataFrame(Forecastdf_row).transpose()])
    CurrentForecastDF = new_df
    return CurrentForecastDF

if __name__ == '__main__':
    CurrentForecastDF = ForecastFetch()
    CurrentForecastDF.to_csv('CurrentForecast.csv')

##########################################################################

### Reading Wind data and preparing Wind dataframe

## Reading Wind Direction data and preparing Wind Direction dataframe
