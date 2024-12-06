from forecastfetch import ForecastFetch

def CollectData():
    '''
    Pulls data from ForecastFetch() and isolates time that forecast was
    updated and valid period of the forecast and packages it into 
    a list
    '''
    FullData = ForecastFetch()
    UpdateTime = FullData['timestamp']
    ValidPeriod = FullData['valid_period']
    TampinesForecast = FullData[FullData['area'] == 'Tampines']['forecast'].iloc[0]

    return [UpdateTime.iloc[0], ValidPeriod.iloc[0], TampinesForecast]

if __name__ == '__main__':
    CollectData()