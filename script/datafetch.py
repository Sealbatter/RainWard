'''
This script pulls current precipitation readings from the Singapore's rain gauge network and
packages it into a nice Pandas DataFrame.

All data are from automated weather stations, in contrary to the doppler weather radar 
visualisation provided on https://www.weather.gov.sg/weather-rain-area-50km/
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

def PrecipFetch():
    '''
    Fetches the accumulated precipitation from Singapore's rain gauge network over the past 5 minutes.
    '''

    def MetadataDF_Constructor(metadata: list):
        data = {'id': [], 'name': [], 'latitude': [], 'longitude': []}
        for dict in metadata:
            data['id'].append(dict['id'])
            data['name'].append(dict['name'])
            data['latitude'].append(dict['location']['latitude'])
            data['longitude'].append(dict['location']['longitude'])
        return pd.DataFrame(data=data)

    logging.basicConfig(level=logging.INFO)

    url = 'https://api-open.data.gov.sg/v2/real-time/api/rainfall'
    response = requests.get(url)
    rawdata = response.json()
    try:
        value = rawdata['data']['readings'][0]['data']
        timestamp = rawdata['data']['readings'][0]['timestamp']
        metadata = rawdata['data']['stations']

        MetaData = MetadataDF_Constructor(metadata)

        StationList = [dict['stationId'] for dict in value]
        ValueList = [dict['value'] for dict in value]
        timestampList = [timestamp for dict in value]

        data = {'timestamp': timestampList, 'stations': StationList, 'values': ValueList}
        CurrentPrecipDF = pd.DataFrame(data=data)

        # Adding coordinate information into CurrentPrecipDF
        new_df = pd.DataFrame(columns=['timestamp', 'stations', 'values', 'latitude', 'longitude'])
        for precipmetadf_row in MetaData.iterrows():
            for precipdf_row in CurrentPrecipDF.iterrows():
                if precipmetadf_row[1]['id'] == precipdf_row[1]['stations']:
                    latlongseries = pd.Series(data=[precipmetadf_row[1]['latitude'], precipmetadf_row[1]['longitude']], index=['latitude', 'longitude'])
                    precipdf_row = pd.concat([precipdf_row[1], latlongseries])
                    new_df = pd.concat([new_df, pd.DataFrame(precipdf_row).transpose()])
        CurrentPrecipDF = new_df
        return CurrentPrecipDF
    
    except TypeError:
        logging.info(rawdata['errorMsg'])


if __name__ == '__main__':
    CurrentPrecipDF = PrecipFetch()

##########################################################################

### Reading Wind data and preparing Wind dataframe

## Reading Wind Direction data and preparing Wind Direction dataframe
